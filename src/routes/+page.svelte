<script lang="ts">
    import Question from "./Question.svelte";
    let number = 30;
    let cnt = 0;
</script>
<h1 class="text-3xl font-bold underline">
    Hello world!
</h1>
<br>
<br>
<Question number={++cnt} />    

