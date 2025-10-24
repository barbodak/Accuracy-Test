<script lang="ts">
    import { cardData } from "$lib/card-data";
    import { createEventDispatcher } from "svelte";

    export let id: number;
    $: card = cardData[id];

    const dispatch = createEventDispatcher();
</script>

<!-- 
  w-full و h-full تضمین می‌کنند که این کامپوننت فضای کامل سلول گرید والد خود را پر می‌کند.
  overflow-hidden از سرریز شدن محتوا جلوگیری می‌کند.
-->
<div
    class="w-full h-full flex flex-col bg-white rounded-lg shadow-md hover:shadow-xl hover:-translatey-1 transition-all duration-200 overflow-hidden border border-slate-200 select-none relative group"
>
    <!-- دکمه حذف -->
    <button
        on:click|stopPropagation={() => dispatch("remove")}
        class="absolute top-1 right-1 z-10 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center
           opacity-0 group-hover:opacity-100 transition-opacity duration-200
           hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400"
        aria-label="Remove card"
    >
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="3"
            stroke-linecap="round"
            stroke-linejoin="round"
            ><line x1="18" y1="6" x2="6" y2="18"></line><line
                x1="6"
                y1="6"
                x2="18"
                y2="18"
            ></line></svg
        >
    </button>

    <!-- بخش بالایی با حرف -->
    <div
        class="flex-shrink-0 bg-slate-50 pt-2 pb-1 flex items-center justify-center"
    >
        <span
            class="text-4xl sm:text-5xl font-bold text-slate-700"
            style="text-shadow: 1px 1px 3px rgba(0,0,0,0.1);"
        >
            {card.letter}
        </span>
    </div>

    <!-- خط جداکننده -->
    <div class="h-px bg-slate-200"></div>

    <!-- 
    بخش پایینی با متن
    - flex-grow باعث می‌شود این بخش فضای باقیمانده را پر کند.
    - overflow-auto باعث می‌شود که اگر متن طولانی‌تر از فضای موجود باشد،
      یک اسکرول‌بار داخلی اضافه شود و خود کارت بزرگ‌تر نشود.
      این کار از به هم ریختن چیدمان گرید جلوگیری می‌کند.
  -->
    <div
        class="flex-grow flex flex-col items-center justify-center p-4 text-center overflow-auto"
    >
        <p class="text-xs sm:text-sm text-slate-500 mb-3 leading-tight">
            {card.prompt}
        </p>
        <p
            class="text-sm sm:text-base font-semibold text-slate-800 leading-relaxed"
        >
            {card.text}
        </p>
    </div>
</div>
