<script lang="ts">
	const options = ['A', 'B', 'C', 'D'];
	let selected = '0';
	export let number: Number;
		// function selection() {

		// }
</script>

<div class="flex flex-row h-44 w-screen justify-center my-10">
	<p class="text-5xl mx-10 my-14 text-cyan-900">{number}</p>
	<img src="src/images/q1.jpg" class="border-4 border-black m-10 h-44" >
	{#each options as option}
		<button
			on:click={() => 
				{selected = option}
			}
			>
		<img src="src/images/q1a{option}.jpg" class=" my-10 mx-3 border-4 h-44 {selected === option? "border-blue-500": "border-greay-600"} ">
	</button>
	{/each}
</div>

