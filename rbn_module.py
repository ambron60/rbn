import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class RBN:
    def __init__(self, nodes, min_k=1, max_k=20, topology=None):
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
        self.functions = self.boolean_functions()

    def __getitem__(self, node):
        return self.state[node]

    def random_topology(self):
        topology = {}
        for node in range(1, self.nodes + 1):
            num_influences = random.randint(self.min_k, self.max_k)
            influences = random.sample(range(1, self.nodes + 1), num_influences)
            if node in influences:
                influences.remove(node)  # Prevent self-loops
            topology[node] = influences
        return topology

    def boolean_functions(self):
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

        def nand_function(inputs):
            return not all(inputs)

        def nor_function(inputs):
            return not any(inputs)

        def random_function(inputs):
            return random.choice([True, False])

        def majority_function(inputs):
            return inputs.count(True) > len(inputs) // 2

        def parity_function(inputs):
            return sum(inputs) % 2 == 1

        possible_functions = [
            and_function, or_function, identity_function, parity_function
        ]
        return {node: random.choice(possible_functions) for node in self.topology.keys()}

    def apply_noise(self, noise_level=0.10):
        """
        Introduce noise by randomly flipping the state of some nodes.
        :param noise_level: Probability of flipping each node's state.
        """
        for node in self.state.keys():
            if random.random() < noise_level:
                self.state[node] = 1 - self.state[node]

    def update_network(self):
        """
            Update the network state based on the current topology and Boolean functions.
        """
        new_state = {}
        for node, inputs in self.topology.items():
            input_states = [self.state[i] for i in inputs]
            new_state[node] = self.functions[node](input_states)

        # Apply noise after updating the state (optional)
        self.apply_noise(noise_level=0.10)

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

        # Create a custom colormap: gray for 0 and blue for 1 with higher contrast
        cmap = mcolors.ListedColormap(['gray', 'blue'])
        bounds = [-0.5, 0.5, 1.5]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        # Set up the figure and axis
        fig, ax = plt.subplots(figsize=(14, 10))

        # Use pcolormesh to plot the data, ensuring each state is one rectangle
        mesh = ax.pcolormesh(data.T, cmap=cmap, norm=norm, edgecolors='black', linewidth=0.5)

        # Invert the y-axis so that Node 1 is on top
        ax.invert_yaxis()

        # Add y-ticks for nodes
        ax.set_yticks(np.arange(0.5, len(nodes), 1))
        ax.set_yticklabels([f"Node {node}" for node in nodes])

        # Set the labels and title
        plt.xlabel("Time Step")
        plt.ylabel("Node")
        plt.colorbar(mesh, label="State (0=gray, 1=blue)", ticks=[0, 1])
        plt.title("RBN State Evolution (Gray = 0, Blue = 1)\n")
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