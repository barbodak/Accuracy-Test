<script lang="ts">
    export let canBeExited: boolean;
    export let isTransparent: boolean;
</script>

<div
    on:click
    role="button"
    class={"w-screen h-screen fixed top-0 left-0 flex justify-center items-center " +
        (isTransparent ? "bg-black bg-opacity-60" : "")}
>
    <div class="relative flex flex-col justify-center items-center max-w-lg">
        <div
            class={"bg-slate-800 text-white rounded-lg shadow-2xl flex flex-col justify-center items-center max-w-lg" +
                (canBeExited ? "" : " px-8 py-5")}
        >
            <slot />
        </div>
    </div>
</div>
