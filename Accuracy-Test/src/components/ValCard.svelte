<script lang="ts">
    import Overlay from "./Overlay.svelte";

    export let id: number;
    let wasDoubleClicked = false;
    let name = String.fromCharCode("A".charCodeAt(0) + id);
</script>

<div class="" draggable={true} on:dragstart role="button" tabindex="0">
    <button on:click on:dblclick={() => (wasDoubleClicked = true)}>
        <img src="/images/cards/{name}.jpg" alt={name} />
        {#if wasDoubleClicked}
            <Overlay
                canBeExited={true}
                isTransparent={true}
                on:click={() => (wasDoubleClicked = false)}
            >
                <img src="/images/cards/{name}.jpg" alt={name} />
            </Overlay>
        {/if}
    </button>
</div>
