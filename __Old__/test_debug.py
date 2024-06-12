import pandas as pd
import random

data = pd.read_parquet(r"Netflix_Prize_data\netflix_data_sample.parquet")



import random
import numpy as np


class Environment:
    def __init__(self, data):
        # el ambiente tiene en memoria el dataframe con los datos de las interacciones de usuarios
        self.data = data

        # se escoge como punto de partida cualquier contenido movie_id
        self.initial_state = data.sample(1)["movie_id"].iloc[0]

        # se inicializa el estado actual con el estado inicial
        self.state = self.initial_state

        # strikes controla la terminación del episodio, 3 strikes y el episodio termina
        self.strikes = 0
        # recompensa por defecto si se llega a 3 strikes, está fuera (out)
        self.reward_out = -10



    def reset_strikes(self):
        self.strikes = 0
       
    def is_terminal(self):
        return self.strikes == 2

    def get_current_state(self):
        """
        Retorna el estado actual (el movie_id actual)

        Returns
        -------
        int
            Identificador de la película actual (movie_id)
        """
        return self.state

    # def get_movie_name(self, movie_id):
    #     """
    #     Retorna el nombre de la película dado el movie_id

    #     Parameters
    #     ----------
    #     movie_id : int
    #         Identificador de la película

    #     Returns
    #     -------
    #     str
    #         Nombre de la película
    #     """
    #     return self.data[self.data["movie_id"]==movie_id]["movie_title"].iloc[0]


    def get_possible_actions(self, state):
        """
        Retorna las acciones posibles dado un estado (movie_id), 
        las acciones serán cambiar a otro contenido dentro de los candidatos, los cuales son el grupo de películas con mejor calificación
        media del usuario que ha calificado la película actual
        """
        # obtener las películas candidatas, puntuación media dadas por los usuarios que vieron el contenido actual
        candidates = data[data.movie_id == state].groupby("best_movie_id")["best_rating"].mean().sort_values(ascending=False)
        # filtro para que solo se escojan las películas con mayor rating dentro del grupo de candidatos
        candidates = candidates[(candidates==candidates.max())].index

        return candidates
    
    def do_action(self, action):
        
        reward = 0
        done = False

        if self.is_terminal():
            reward = self.reward_out
            done = True
        else:
            # se obtiene la calificación media de los usuarios que vieron el contenido a recomendar
            rating = self.data[self.data.movie_id == action].rating.mean()
            # se escala la recompensa en función de la calificación media
            reward = self.reward_scalation(rating)

            # si el contenido recomendado tiene una calificación media menor a 3, se considera un strike para el agente,
            # de lo contrario se reinician los strikes
            if reward<0:
                self.strikes += 1
            else:
                self.reset_strikes()

        # recordar que la acción es el cambio de contenido, el nuevo estado es el nuevo contenido (id_movie a recomendar)
        self.state = action
        return reward, self.state, done


    def reward_scalation(self, rating):
        # la escala retorna 1 si el rating medio es 5, 0 si es 3 y -1 si es 1
        return (rating-3)/2


    def reset(self):
        self.state = self.initial_state



# agente



import numpy as np
import random
import copy
        
class Agent:
    def __init__(self, env, gamma=0.9, alpha=0.1, epsilon=0.9, episodes=1000):

        # el agente tiene en memoria el ambiente
        self.environment = env
        # gamma factor de descuento
        self.gamma = gamma
        # alpha tasa de aprendizaje
        self.alpha = alpha
        # epsilon factor de exploración
        self.epsilon = epsilon
        # decay_rate tasa de decaimiento de epsilon
        self.decay_rate = 0.9

        # número de episodios
        self.episodes = episodes
        # Q table inicializada como un diccionario vacío, los estados y acciones se irán añadiendo a medida que se vayan explorando (evita crear una tabla muy grande)
        self.qtable ={}


    def run(self):

        for episode in range(self.episodes):
            self.environment.reset()
            # estado actual (movie_id actual)
            state = self.environment.get_current_state()
            # done indica si el episodio ha terminado (si el agente ha llegado a 3 strikes)
            done = False

            while not done:
                # se escoge una acción (cambio de contenido) al azar o con base en la Q table determinado por epsilon
                action = self.random_action(state)

                reward, next_state, done = self.step(action)
                
                # si el estado no está en la Q table, se añade
                if state not in self.qtable:
                    self.qtable[state] = {action: 0}
                else:
                    # si la acción no está en la Q table, se añade
                    if action not in self.qtable[state]:
                        self.qtable[state][action] = 0

                # valor del estado actual en la Q table
                old_value = self.qtable[state][action]
                # valor del estado siguiente en la Q table
                next_max = max(self.qtable[next_state].values()) if next_state in self.qtable else 0
                # cálculo del nuevo valor del estado actual con base en la ecuación de Bellman
                new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)


                if action is not None:
                    self.qtable[state][action] = new_value
                else:
                    self.qtable[state][action] = reward
                    
                state = next_state
            
            self.epsilon = max(self.epsilon * self.decay_rate,0.01)


    def random_action(self, current_state):

        possible_actions = self.environment.get_possible_actions(current_state)

        # fase de exploración (adquirir conocimiento)
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(possible_actions)
        
        # fase de explotación del conocimiento
        else:
            # si aún no tiene conocimiento del estado actual, se escoge una al azar    
            if ~ (current_state in self.qtable.keys()):
                best_action = random.choice(possible_actions)

            # si ya tiene conocimiento, se escoge la acción con mayor valor
            else:
                max_value = max(self.qtable[current_state].values())
                max_keys = [key for key, value in self.qtable[current_state].items() if value == max_value]
                best_action = random.choice(max_keys)

            return best_action



    
    def step(self, action):
       
        return self.environment.do_action(action)
    
    
    # def actions_values(self):

    #     actions = {}
    #     values = np.zeros((self.environment.nrows, self.environment.ncols))
    #     for state, action_values in self.qtable.items():
    #         i, j = state
    #         actions[state] = max(action_values, key=action_values.get)
    #         values[i][j] = max(action_values.values())
    #     return actions, values
        

        
    # def max_action(self, current_state):
    #     action_index = np.argmax(self.qtable[current_state]) 
    #     actions = self.environment.actions
    #     return actions[action_index]

    # def action_name(self, action_index):
    #     return self.environment.actions[action_index]
    
    # def action_index(self, action):
    #     actions = self.environment.actions
    #     for i in range(len(actions)):
    #         if actions[i] == action:
    #             return i
    #     return -1



env = Environment(data)

#creación del agente
agent = Agent(env, gamma=0.9, alpha=0.1, epsilon=0.9, episodes=500)
#ejecución del agente
agent.run()
# actions, values = agent.actions_values()
# env.plot_action(actions, values)