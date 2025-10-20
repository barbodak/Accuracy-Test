<script lang="ts">
	export let selected = '0';
	export let number: number;
	const options = ['A', 'B', 'C', 'D'];
	const selection = (option: string) => {
		selected = selected === option ? '0' : option;
	};
	// Using original image paths
	const getImageUrl = (type: 'question' | 'option', optionChar = '') => {
		if (type === 'question') {
			return `/images/quiz/${number}.png`;
		}
		return `/images/quiz/${number}${optionChar}.png`;
	};
</script>

<div class="bg-white rounded-lg overflow-hidden p-4 sm:p-6 transition-shadow hover:shadow-lg">
	<!-- <h2 class="text-lg sm:text-xl font-bold text-slate-700 mb-2 truncate"> -->
	<!-- 	<span class="text-indigo-600">{number}</span>. -->
	<!-- </h2> -->

	<div class="flex w-full items-center gap-3 sm:gap-4">
		<div
			class="aspect-square rounded-md border-2 ring-black border-slate-400 p-1"
			style="flex: 1.1 1 0%;"
		>
			<img
				src={getImageUrl('question')}
				class="w-full h-full object-contain"
				alt={`Question Number ${number}`}
				loading="lazy"
			/>
		</div>

		{#each options as option}
			<button
				on:click={() => selection(option)}
				class="relative rounded-md transition-all duration-200 focus:outline-none focus-visible:ring-4 focus-visible:ring-offset-2 focus-visible:ring-indigo-300"
				class:border-indigo-500={selected === option}
				class:border-4={selected === option}
				class:border-slate-300={selected !== option}
				class:border-2={selected !== option}
				class:hover:border-indigo-500={selected !== option}
				style="flex: 1 1 0%;"
			>
				<div class="aspect-square bg-white flex items-center justify-center">
					<img
						src={getImageUrl('option', option)}
						class="w-full h-full object-contain p-1"
						alt={`Option ${option} for Question ${number}`}
						loading="lazy"
					/>
				</div>
				{#if selected === option}
					<div
						class="absolute -top-3 -right-3 flex items-center justify-center w-6 h-6 bg-indigo-500 rounded-full text-white font-bold ring-2 ring-white"
					>
						✓
					</div>
				{/if}
			</button>
		{/each}
	</div>
</div>
