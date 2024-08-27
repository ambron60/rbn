from rbn_module import RBN


if __name__ == "__main__":
    # Create an RBN with 15 nodes and random K between 1 and x
    rbn = RBN(nodes=15, min_k=5, max_k=10)

    for node, inputs in rbn.topology.items():
        print(f"Node {node} has {len(inputs)} inputs.")

    # Simulate the RBN for x steps
    history = rbn.simulate(steps=500)

    # Plot the history of states using the custom heatmap
    rbn.plot_history(history)