<script lang="ts">
    import Question from "./Question.svelte";
    let number = 30;
    let cnt = 0;
    let isOverlayOpen = false;
</script>
<h1 class="text-3xl font-bold underline">
    Hello world!
</h1>
<br>
<br>
<div>
{#each Array(50) as _, index (index)}
        <Question number={index} />    
{/each}
</div>
<br>
<br>
<br>
<br>
<button>
    turn on the overlay
</button>