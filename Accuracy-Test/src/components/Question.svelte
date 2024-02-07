<script lang="ts">
	const options = ["A", "B", "C", "D"];
	export let selected = "0";
	export let number: Number;
	const selection = function (option: string) {
		selected === option ? (selected = "0") : (selected = option);
	};
</script>

<div class="flex flex-row h-44 w-screen justify-center my-10">
	<!-- <p class="text-5xl mx-10 my-14 text-cyan-900">{number}</p> -->
	<img
		src="/images/quiz/{number}.png"
		class="border-4 border-black m-10 h-44"
		alt={"Question Number " + number.toString}
	/>
	{#each options as option}
		<button
			on:click={() => {
				selection(option);
			}}
		>
			<img
				src="/images/quiz/{number}{option}.png"
				class=" my-10 mx-3 border-4 h-44 {selected === option
					? 'border-blue-500'
					: 'border-greay-600'} "
				alt={"Option " + option + " of Questoin " + number.toString}
			/>
		</button>
	{/each}
</div>
