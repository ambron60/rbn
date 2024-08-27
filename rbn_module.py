import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class RBN:
    def __init__(self, nodes, min_k=1, max_k=2, topology=None):
        """
        Initialize the Random Boolean Network.

        :param nodes: Number of nodes in the network.
        :param min_k: Minimum number of inputs (K) each node can have.
        :param max_k: Maximum number of inputs (K) each node can have.
        :param topology: Optional predefined topology. If None, a random topology will be generated.
        """
        # Ensure max_k does not exceed the number of available nodes
        if max_k >= nodes:
            raise ValueError(f"max_k ({max_k}) cannot be greater than or equal to the number of nodes ({nodes}).")

        self.nodes = nodes
        self.min_k = min_k
        self.max_k = max_k
        self.state = {node: random.choice([0, 1]) for node in range(1, nodes + 1)}
        self.topology = topology if topology else self.random_topology()
        self.functions = self.random_functions()

    def __getitem__(self, node):
        return self.state[node]

    def random_topology(self):
        """
        Generate a random topology where each node is influenced by a random number of other nodes.
        """
        topology = {}
        for node in range(1, self.nodes + 1):
            # Randomly assign K influences between min_k and max_k
            num_influences = random.randint(self.min_k, self.max_k)
            influences = random.sample(range(1, self.nodes + 1), num_influences)
            topology[node] = influences
        return topology

    # Uncomment and use the below for a fixed K on each node.
    # def random_topology(self):
    #     topology = {}
    #     for node in range(1, self.nodes + 1):
    #         influences = random.sample(range(1, self.nodes + 1), 5)  # Fixed K = 5
    #         topology[node] = influences
    #     return topology

    def random_functions(self):
        """
        Randomly assign a Boolean function to each node.
        """

        def and_function(inputs):
            return all(inputs)

        def or_function(inputs):
            return any(inputs)

        def not_function(inputs):
            return not inputs[0] if inputs else False

        def xor_function(inputs):
            if len(inputs) == 2:
                return inputs[0] != inputs[1]
            elif len(inputs) == 1:
                return inputs[0]
            else:
                return False

        def identity_function(inputs):
            return inputs[0] if inputs else False

        # def complex_function(inputs):
        #     mid = len(inputs) // 2
        #     return xor_function(inputs[:mid]) or and_function(inputs[mid:])

        possible_functions = [and_function, or_function, not_function, xor_function, identity_function]
        return {node: random.choice(possible_functions) for node in self.topology.keys()}

    def update_network(self):
        """
        Update the network state based on the current topology and Boolean functions.
        """
        new_state = {}
        for node, inputs in self.topology.items():
            input_states = [self.state[i] for i in inputs]
            new_state[node] = self.functions[node](input_states)
        self.state = new_state

    def simulate(self, steps):
        """
        Simulate the network over a given number of time steps.

        :param steps: Number of steps to simulate.
        :return: A list of network states over time.
        """
        history = [self.state.copy()]
        for _ in range(steps):
            self.update_network()
            history.append(self.state.copy())
        return history

    @staticmethod
    def plot_history(history):
        """
        Plot the history of network states using pcolormesh.

        :param history: A list of network states over time.
        """
        nodes = sorted(history[0].keys())
        time_steps = len(history)
        data = np.array([[history[t][node] for node in nodes] for t in range(time_steps)])

        # Create a custom colormap: red for 0 and blue for 1 with higher contrast
        cmap = mcolors.ListedColormap(['red', 'blue'])
        bounds = [-0.5, 0.5, 1.5]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        # Set up the figure and axis
        fig, ax = plt.subplots(figsize=(14, 10))

        # Use pcolormesh to plot the data, ensuring each state is one rectangle
        mesh = ax.pcolormesh(data.T, cmap=cmap, norm=norm, edgecolors='black', linewidth=0.5)

        # Invert the y-axis so that Node 1 is on top
        ax.invert_yaxis()

        # Add top ticks without labels
        ax.tick_params(axis='x', which='both', top=True, bottom=False, labeltop=False)
        ax.set_xticks(np.arange(0.5, time_steps, 1))  # Tick marks in the center of each time step
        ax.set_xticklabels([''] * time_steps)

        # Add y-ticks for nodes
        ax.set_yticks(np.arange(0.5, len(nodes), 1))
        ax.set_yticklabels([f"Node {node}" for node in nodes])

        # Set the labels and title
        plt.xlabel("Time Step")
        plt.ylabel("Node")
        plt.colorbar(mesh, label="State (0=red, 1=blue)", ticks=[0, 1])
        plt.title("RBN State Evolution (Red = 0, Blue = 1)\n")
        plt.show()

    @staticmethod
    def print_state_table(history):
        """
        Print the state of each node over time in a table-like format.

        :param history: A list of network states over time.
        """
        nodes = sorted(history[0].keys())
        time_steps = len(history)

        # Create a 2D array to represent the states of each node over time
        state_matrix = np.array([[history[t][node] for t in range(time_steps)] for node in nodes])

        # Print the header (time steps)
        header = "Time Step | " + " ".join([f"{t:3}" for t in range(time_steps)])
        print(header)
        print("-" * len(header))

        # Print each node's state over time
        for i, node in enumerate(nodes):
            row = f"Node {node:2}  | " + " ".join([f"{state_matrix[i, t]:3}" for t in range(time_steps)])
            print(row)