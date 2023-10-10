<script lang="ts">
    import Layout from "../+layout.svelte";
    import ValCard from "../../components/ValCard.svelte";
    let answers = Array(20).fill(0);
    let cardWasUsed = Array(20).fill(false);
</script>
<div class="absolute top-0 right-0 h-screen w-1/5 bg-blue-950 overflow-auto">
    {#each cardWasUsed as card, index}
    {#if card === false}
    <ValCard name = {String.fromCharCode('A'.charCodeAt(0) + index)}></ValCard>
    {/if}
    {/each}
</div>
<div class="absolute top-0 left-0 h-screen w-4/5">
    <h1>ستون سمت راست فقط اسکرول می‌شه</h1>
    <div class="grid grid-cols-5 gap-4 mx-5">
        {#each answers as answer}
            <div class="bg-black rounded-md">
                test
            </div>
        {/each}
    </div>
</div>