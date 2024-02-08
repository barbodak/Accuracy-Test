<script lang="ts">
    import Overlay from "./Overlay.svelte";

    export let id: number;
    let name = String.fromCharCode("A".charCodeAt(0) + id);
</script>

<div class="" draggable={true} on:dragstart role="button" tabindex="0">
    <button on:click>
        <img src="/images/cards/{name}.jpg" alt={name} />
        <!-- <Overlay canBeExited={true} isTransparent={false}> -->
        <!--     <img src="/images/cards/{name}.jpg" alt={name} /> -->
        <!-- </Overlay> -->
    </button>
</div>
