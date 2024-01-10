<script lang="ts">
    import { writable } from "svelte/store";
    import Layout from "../+layout.svelte";
    import ValCard from "../../components/ValCard.svelte";
    import Page from "../+page.svelte";
    let answers = Array(20).fill(0);
    let cardWasUsed = Array(20).fill(false);
    let txt = "no touching yet";
    let hoveringOver = 90;

    function handleDragStart(event : DragEvent, cardIndex: number) {
            event.dataTransfer?.setData('cardName', cardIndex.toString());
    }
    function handleDrop(event :any, dropZoneIndex: number) {
        event.preventDefault();
        if (answers[dropZoneIndex] === 0) {
            const  cardIndex = parseInt(event.dataTransfer.getData("cardName"));
            txt = cardIndex.toString();
            // Remove the item from one basket.
            // Splice returns an array of the deleted elements, just one in this case.
            cardWasUsed[cardIndex] = true;
            answers[dropZoneIndex] = 0;
            answers[dropZoneIndex] = cardIndex;
            hoveringOver = 100;
        }
    } 
</script>

<p> {txt} </p>
<p> {hoveringOver} </p>
<div class="absolute top-0 right-0 h-screen w-1/5 bg-blue-950 overflow-auto" 
    on:touchend={(e) => {txt = "YOU TOUCHED !";}}>
    {#each cardWasUsed as card, index}
        {#if card === false}
            <div  class="mx-5 my-7" draggable={true} on:dragstart={event => handleDragStart(event, index)}>
                <ValCard id = {index} ></ValCard>
            </div>
        {/if}
    {/each}
</div>
<div class="absolute top-0 left-0 h-screen w-4/5">
    <div class="grid grid-cols-5 gap-x-5 gap-y-6 h-screen p-5">
        {#each answers as answer, index}
            <div class={"border-2 border-solid rounded-md text-center place-items-center " + ((hoveringOver === index)? "border-orange-600": "border-black")}
                on:dragenter={() => hoveringOver = index}
                on:dragleave={() => hoveringOver = 100}
                on:drop={event => handleDrop(event, index)}
                on:dragover={(ev) => { ev.preventDefault() }}>
                {#if answers[index] === 0}

                {:else}
                    <ValCard id = {answers[index]}></ValCard>
                {/if}
            </div>
        {/each}
    </div>
</div>
