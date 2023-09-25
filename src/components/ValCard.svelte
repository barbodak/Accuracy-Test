<script lang="ts">
    import Overlay from "./Overlay.svelte";

    export let name: String;
    let wasClicked = false;
</script>

<div class="mx-5 my-7">
    <button on:click={()=>wasClicked = true}>
        <img src="src/images/cards/{name}.jpg" />
        {#if wasClicked === true}
            <Overlay>
                <img src="src/images/cards/{name}.jpg" />
            </Overlay>
        {/if}
    </button>
</div>
