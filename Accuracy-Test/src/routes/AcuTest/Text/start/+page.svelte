<script lang="ts">
    import Overlay from "$lib/../components/Overlay.svelte";
    import { startQuiz } from "$lib/utils/api/quiz-apis";
    const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
    let promise: Promise<void>;
    const startQuizHandler = async () => {
        promise = startQuiz({
            quiz_type: "AcuTest_text",
        });
        await promise;
        window.location.href = "/AcuTest/Text";
    };
</script>

<Overlay isTransparent={false} canBeExited={false}>
    <p class="text-xl mb-4">Welcome to the Accuracy Test</p>
    <p>ACUTEST is a test that measures your accuracy in answering questions.</p>
    <p>these arethe rules</p>
    <p>-rule 1</p>
    <p>-rule 2</p>
    <p>-rule 3</p>
    <p>{"Good luck :)"}</p>
    <button
        on:click={startQuizHandler}
        class="bg-green-600 hover:bg-green-900 text-white font-bold py-2 px-4 rounded inline-block mt-2"
    >
        شروع
    </button>
</Overlay>
