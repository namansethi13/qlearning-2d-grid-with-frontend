<script>
    import { writable } from 'svelte/store';

    // Define fixed configuration
    const startState = [0, 0];
    const goalState = [4, 4];
    const gridSize = [5, 5];
    const discountFactor = 0.5;
    const learningRate = 0.1;
    let episodes = 1000;
    let policy = [];
    const grid = writable(
        Array.from({ length: gridSize[0] }, () =>
            Array.from({ length: gridSize[1] }, () => -1)
        )
    );

    function handleCellClick(row, col) {
        grid.update(currentGrid => {
            const updatedGrid = currentGrid.map(row => [...row]);

            if ((row === startState[0] && col === startState[1]) || (row === goalState[0] && col === goalState[1])) {
                return updatedGrid;
            }

            updatedGrid[row][col] = updatedGrid[row][col] === -1000 ? -1 : -1000;
            return updatedGrid;
        });
    }

    async function handleSubmit() {
        const environment = $grid; 
        const data = {
            grid_size: gridSize,
            start_state: startState,
            goal_state: goalState,
            discount_factor: discountFactor,
            learning_rate: learningRate,
            environment,
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/init', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                alert('Setup initialized successfully!');
            } else {
                alert('Failed to initialize setup.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during initialization.');
        }
    }

    const handleTrain = async () => {
      const data = {
        episodes: episodes,
      };
      try {
        const response = await fetch('http://127.0.0.1:5000/train', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });
  
        if (response.ok) {
          alert('Training started successfully!');
          const policyResponse = await fetch('http://127.0.0.1:5000/policy');
        
            const policyData = await policyResponse.json();
            policy = policyData.optimal_policy;

        } else {
          alert('Failed to start training.');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while training.');
      }
    };
</script>

<div class="p-8 max-w-4xl mx-auto bg-gray-100 shadow-md rounded-md">
    <h1 class="text-2xl font-bold mb-4">Q-Learning Setup</h1>

    <!-- Display Configuration -->
    <div class="space-y-4">
        <div><strong>Grid Size:</strong> {gridSize[0]} x {gridSize[1]}</div>
        <div><strong>Start State:</strong> [{startState[0]}, {startState[1]}]</div>
        <div><strong>Goal State:</strong> [{goalState[0]}, {goalState[1]}]</div>
        {#if policy.length > 0}
            <p><strong>Optimal Policy:</strong> {policy}</p>
        {/if}
    </div>

    <!-- Grid -->
    <div class="mt-8 bg-white p-4 rounded-md shadow">
        <h2 class="text-xl font-bold mb-4">Environment Grid</h2>
        <div
            class="grid gap-1"
            style="grid-template-columns: repeat({gridSize[1]}, minmax(0, 1fr));"
        >
            {#if $grid && $grid.length > 0}
                {#each $grid as row, rowIndex}
                    {#each row as cell, colIndex}
                        <div
                            class="aspect-square border border-gray-300 cursor-pointer relative transition-colors duration-200 hover:bg-gray-100"
                            style="background-color: {cell === -1000 ? '#FCA5A5' : rowIndex === goalState[0] && colIndex === goalState[1] ? '#86EFAC' : 'white'};"
                            on:click={() => handleCellClick(rowIndex, colIndex)}
                        >
                            {#if rowIndex === startState[0] && colIndex === startState[1]}
                                <span class="absolute top-1 left-1 text-xs font-bold text-blue-600">S</span>
                            {/if}
                            {#if rowIndex === goalState[0] && colIndex === goalState[1]}
                                <span class="absolute bottom-1 right-1 text-xs font-bold text-green-600">G</span>
                            {/if}
                        </div>
                    {/each}
                {/each}
            {/if}
        </div>
    </div>

    <!-- Submit Button -->
    <button
        class="mt-8 w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring focus:ring-blue-300"
        on:click|preventDefault={handleSubmit}
    >
        Initialize Setup
    </button>



    <form on:submit|preventDefault={handleTrain} class="space-y-4">
        <div>
          <label class="block font-medium mb-1">Episodes:</label>
          <input
            type="number"
            bind:value={episodes}
            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300"
            required
          />
        </div>
    
        <button
          type="submit"
          class="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring focus:ring-blue-300"
        >
          Train
        </button>
      </form>
</div>
