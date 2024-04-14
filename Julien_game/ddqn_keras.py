from keras.layers import Dense, Activation
from keras.models import Sequential
from keras.saving import load_model
from keras.optimizers import Adam
import numpy as np
import tensorflow as tf

class ReplayBuffer(object):
    def __init__(self, max_size, input_shape, n_actions, discrete=False):
        self.mem_size = max_size
        self.mem_cntr = 0
        self.discrete = discrete
        self.state_memory = np.zeros((self.mem_size, input_shape))
        self.new_state_memory = np.zeros((self.mem_size, input_shape))
        dtype = np.int8 if self.discrete else np.float32
        self.action_memory = np.zeros((self.mem_size, n_actions), dtype=dtype)
        self.reward_memory = np.zeros(self.mem_size)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.float32)

    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        # store one hot encoding of actions, if appropriate
        if self.discrete:
            actions = np.zeros(self.action_memory.shape[1])
            actions[action] = 1.0
            self.action_memory[index] = actions
        else:
            self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.terminal_memory[index] = 1 - done
        self.mem_cntr += 1

    def sample_buffer(self, batch_size):
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, batch_size)

        states = self.state_memory[batch]
        actions = self.action_memory[batch]
        rewards = self.reward_memory[batch]
        states_ = self.new_state_memory[batch]
        terminal = self.terminal_memory[batch]

        return states, actions, rewards, states_, terminal



class DDQNAgent(object):
    def __init__(self, alpha, gamma, n_actions, epsilon, batch_size,
                 input_dims, epsilon_dec=0.999995,  epsilon_end=0.10,
                 mem_size=25000, fname='ddqn_model.keras', replace_target=25):
        self.action_space = [i for i in range(n_actions)]
        self.n_actions = n_actions
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_end
        self.batch_size = batch_size
        self.model_file = fname
        self.replace_target = replace_target
        self.memory = ReplayBuffer(mem_size, input_dims, n_actions, discrete=True)
       
        self.brain_eval = Brain(input_dims, n_actions, batch_size)
        self.brain_target = Brain(input_dims, n_actions, batch_size)


    def remember(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def choose_action(self, state):

        state = np.array(state)
        state = state[np.newaxis, :]

        rand = np.random.random()
        if rand < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            actions = self.brain_eval.predict(state)
            action = np.argmax(actions)

        return action

    def learn(self):
        if self.memory.mem_cntr > self.batch_size:
            state, action, reward, new_state, done = self.memory.sample_buffer(self.batch_size)
            
            # action_values = np.array(self.action_space, dtype=np.int8)
            # action_indices = np.dot(action, action_values)

            self.brain_target.model.trainable = True
            self.brain_eval.model.trainable = True


            with tf.GradientTape() as tape:
                pass

            action_values = tf.constant(self.action_space, dtype=tf.int32)
            action_indices = tf.cast(tf.reduce_sum(action * action_values, axis=1), dtype=tf.int32)


            q_next = self.brain_target.predict(tf.convert_to_tensor(new_state, dtype=tf.float32)) # Q_theta_prime
            q_eval = self.brain_eval.predict(tf.convert_to_tensor(new_state, dtype=tf.float32)) # Q_theta
            q_pred = self.brain_eval.predict(tf.convert_to_tensor(state, dtype=tf.float32)) # Q_star

            # max_actions = np.argmax(q_eval, axis=1)
            max_actions = tf.cast(tf.argmax(q_next, axis=1), dtype=tf.int32)

            q_target = tf.identity(q_pred) # Q_star

            batch_index = tf.range(self.batch_size, dtype=tf.int32)

            # q_target[batch_index, action_indices] = reward + self.gamma*q_next[batch_index, max_actions.astype(int)]*done
            # q_target[batch_index, action_indices] = reward + self.gamma*q_eval[batch_index, max_actions]*done
            indices = tf.stack([batch_index, action_indices], axis=1)
            updates = reward + self.gamma * tf.gather_nd(q_eval, tf.stack([batch_index, max_actions], axis=1)) * done
            q_target = tf.tensor_scatter_nd_update(q_target, indices, updates)

            # compute mse loss
            loss = tf.keras.losses.MSE(q_target, q_eval)
            # print(f"loss : {loss}")

            
            # grads = tape.gradient(loss, self.brain_eval.model.trainable_variables)
            # print(f"grads : {grads}")
            # self.brain_eval.model.optimizer.apply_gradients(zip(grads, self.brain_eval.model.trainable_variables))

            # # target network update
            # for target_param, param in zip(self.brain_target.trainable_variables, self.brain_eval.trainable_variables):
            #     target_param.assign(self.tau * param + (1 - self.tau) * target_param)

            _ = self.brain_eval.train(state, q_target)

            self.epsilon = self.epsilon*self.epsilon_dec if self.epsilon > self.epsilon_min else self.epsilon_min


    def update_network_parameters(self):
        self.brain_target.copy_weights(self.brain_eval)

    def save_model(self):
        self.brain_eval.model.save(self.model_file)
        
    def load_model(self):
        self.brain_eval.model = load_model(self.model_file)
        self.brain_target.model = load_model(self.model_file)
       
        if self.epsilon == 0.0:
            self.update_network_parameters()


class Brain:
    def __init__(self, NbrStates, NbrActions, batch_size = 256):
        self.NbrStates = NbrStates
        self.NbrActions = NbrActions
        self.batch_size = batch_size
        self.tau = 0.01
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
        self.model = self.createModel()
    
    def createModel(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu)) #prev 256
        model.add(tf.keras.layers.Dense(512, activation=tf.nn.relu))
        model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
        model.add(tf.keras.layers.Dense(self.NbrActions, activation="softmax"))#tf.nn.softmax)) 
        model.compile(loss = "mse", optimizer=self.optimizer)

        return model
    
    def train(self, x, y, epoch = 5, verbose = 0):
        self.model.fit(x, y, epochs=epoch, batch_size = self.batch_size, verbose = verbose)

    def predict(self, s):
        return self.model.predict(s)

    def predictOne(self, s):
        return self.model.predict(tf.reshape(s, [1, self.NbrStates])).flatten()
    
    def copy_weights(self, TrainNet):
        variables1 = self.model.trainable_variables
        variables2 = TrainNet.model.trainable_variables
        for v1, v2 in zip(variables1, variables2):
            v1.assign(v2.numpy())

