<script lang="ts">
  export let questions: {
    index: number;
    state: "answered" | "skipped" | "unanswered";
    color: string; // Now expects a CSS color/gradient string
    isPartStart: boolean;
  }[] = [];
  export let currentIndex: number = 0;
</script>

<div class="w-full flex items-center justify-center mt-6 mb-4 py-3">
  <div class="relative w-full h-3 bg-white/40 backdrop-blur-sm rounded-full flex shadow-inner">
    
    {#each questions as q, i}
      <div class="relative h-full flex-1 transition-all duration-300
           {q.isPartStart && i !== 0 ? 'border-s-[2.5px] border-white/90' : ''}
           {i === 0 ? 'rounded-s-full' : ''}
           {i === questions.length - 1 ? 'rounded-e-full' : ''}">
           
        <div class="w-full h-full overflow-hidden {i === 0 ? 'rounded-s-full' : ''} {i === questions.length - 1 ? 'rounded-e-full' : ''}">
          {#if q.state === "answered"}
            <!-- Applying the dynamic HSL gradient as an inline style -->
            <div class="w-full h-full" style="background: {q.color};"></div>
          {:else if q.state === "skipped"}
            <!-- Skipped state remains translucent -->
            <div class="w-full h-full opacity-30" style="background: {q.color};"></div>
          {/if}
        </div>

        <!-- Current Marker -->
        {#if i === currentIndex}
          <div class="absolute -top-[5px] -bottom-[5px] -left-[2px] -right-[2px] 
                      border-[2.5px] border-black bg-transparent rounded-md 
                      shadow-[0_2px_4px_rgba(0,0,0,0.15)] 
                      z-20 pointer-events-none">
          </div>
        {/if}
        
      </div>
    {/each}
    
  </div>
</div>

