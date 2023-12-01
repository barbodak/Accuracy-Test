<script lang="ts">
    import { writable } from "svelte/store";
import Layout from "../+layout.svelte";
    import ValCard from "../../components/ValCard.svelte";
    let answers = Array(20).fill(0);
    let cardWasUsed = Array(20).fill(false);
    let txt = "no touching yet";
    let droppedIn : any  = Array(20).fill(false);
    let drop_zone : HTMLElement;


    //drag  shit
    let dropped : any = Array(20);
    let status = '';

    function createHandleDragDrop(index : number) {
        const handleDragDrop = (e : any) => {
            e.preventDefault();
            var element_id = e
            .dataTransfer
            .getData("text");
            dropped[index] = (element_id);
            droppedIn[index] = true;
            status = "You droped " + element_id + " into drop zone";
        }
        return handleDragDrop
    }
    function createHandleTouchEnd(index : number) {
        const handleTouchEnd = (e : any) => {
    	e.preventDefault();
      	let pageX = (parseInt(e.target.style.left) - 50);
      	let pageY = (parseInt(e.target.style.top) - 50);

      	if (detectTouchEnd(drop_zone.offsetLeft, drop_zone.offsetTop, pageX, pageY, drop_zone.offsetWidth, drop_zone.offsetHeight)) {
        	dropped = dropped.concat(e.target.id);
        	e.target.style.position = "initial";
        	droppedIn[index] = true;
        	status = "You dropped " + e
          	.target
          	.getAttribute('id') + " into drop zone";
        } else {
        	e.target.style.left = originalX;
        	e.target.style.top = originalY;
        	status = "You let the " + e
          	.target
          	.getAttribute('id') + " go.";
        }
    }
</script>
<p> {txt} </p>
<div class="absolute top-0 right-0 h-screen w-1/5 bg-blue-950 overflow-auto"
    on:touchend={(e) => {txt = "YOU TOUCHED !";}}>
    {#each cardWasUsed as card, index}
        {#if card === false}
            <ValCard name = {String.fromCharCode('A'.charCodeAt(0) + index)}></ValCard>
        {/if}
    {/each}
</div>
<div class="absolute top-0 left-0 h-screen w-4/5">
    <div class="grid grid-cols-5 gap-x-5 gap-y-6 h-screen p-5">
        {#each answers as answer, index}
            <div class={"border-black border-2 border-solid rounded-md text-center place-items-center " + ((droppedIn[index] === true)? "bg-black": "")} 
                on:drop={createHandleDragDrop(index)}
                bind:this={drop_zone}>
                <p>+</p>
            </div>
        {/each}
    </div>
</div>
