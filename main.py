from rbn_module import RBN


if __name__ == "__main__":
    # Create an RBN with 15 nodes and random K between 1 and x
    rbn = RBN(nodes=20, min_k=2, max_k=4)

    for node, inputs in rbn.topology.items():
        print(f"Node {node} has {len(inputs)} inputs.")

    # Simulate the RBN for x number of steps
    history = rbn.simulate(steps=50)

    # Plot the history of states using the custom heatmap
    rbn.plot_history(history)

    # Print state transition table
    print()
    rbn.print_state_table(history)