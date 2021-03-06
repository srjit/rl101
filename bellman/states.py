import numpy as np
from components import State, Action

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


class StateGraph(object):
    
    def __init__(self, states=[], edges=[], discounting_factor=0.5):
        self._states = states
        self._edges = edges
        self._discounting_factor = discounting_factor


    def add_state(self, state):
        if(type(state) == State):
            self._states.append(state)

    def add_states(self, states):
        list(map(self.add_state, states))
         

    def add_edge(self, edge):
        if(type(edge) == Action):
            self._edges.append(edge)
            

    def add_edges(self, edges):
        list(map(self.add_edge, edges))


       
    def get_all_connected_edges(self, state):
        return [x for x in self._edges if x._source == state]


        
    def get_all_connected_states(self, edges):
        return [x._destination for x in edges]




    def transition_probability_matrix(self):
        return [self._get_tps_of_state(state) for state in self._states]


    ##calculate value function of all states 
    # how good is it to be in a particular state - V
    # state value function
    # top level state value = transtion probability left (left action value) + 
    # transtion probability right (right action value)
    
    # how good is it to take a particular action - q 
    # action value function
    # Value of taking a specific action at a state
    # = (tp of going left * left state value) + (tp of going right * right state value)
    
    # Now V in terms of itself recursively

    def value_function_of_all_states(self):
        tps = self.transition_probability_matrix()
        transition_probability_matrix = np.array(tps)
        num_states = len(self._states)
        tmp = np.linalg.inv(np.identity(num_states) - self._discounting_factor * transition_probability_matrix)
        rewards = [x._reward for x in self._states]
        return rewards - tmp
        


    def get_lookahead_reward(self, action):
        destination = action._destination
        actions_from_destination = self.get_all_connected_edges(destination)
        lookahead_reward = 0

        if len(actions_from_destination) > 0:
            lookahead_reward = sum([action._tp * action._destination._reward for action in actions_from_destination])

        return lookahead_reward



    def bellman_expectation_for_state(self, index):
        state = self._states[index]
        connected_edges = self.get_all_connected_edges(state)

        return sum([action._tp * (action._reward + 
                self.get_lookahead_reward(action)) for action in connected_edges])



    def optimal_action_value_function(self, index):
        """
        
        Arguments:
        - `self`:
        - `index`: Index of the action whose optimal action
        value has to be calculated
        """
        action = self._edges[index]
        states_connected = self.get_all_connected_states(action)

        
        pass




    def optimal_state_value_function(self, index):
        """
        Maximum value function over all policies 
        
        Arguments:
        - `self`:
        - `index`: Index of the state whose optimal 
        value function has to be calculated
        """
        state = self._states[index]
        actions = self.get_all_connected_edges(state)
        
        rewards = [action._destination._reward for action in actions]
        max_reward_index = rewards.index(max(rewards))

          
        return actions[max_reward_index]._destination._reward + actions[max_reward_index]._reward

