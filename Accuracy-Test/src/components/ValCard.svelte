<script lang="ts">
    import Overlay from "./Overlay.svelte";

    export let id: number;
    let name = String.fromCharCode("A".charCodeAt(0) + id);
    let wasClicked = false;
</script>

<div class="max-w-full max-h-full object-contain">
    <button on:click>
        <img src="/images/cards/{name}.jpg" alt={name} />
        {#if wasClicked === true}
            <Overlay canBeExited={true} isTransparent{false}>
                <img src="/images/cards/{name}.jpg" alt={name} />
            </Overlay>
        {/if}
    </button>
</div>
