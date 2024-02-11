<script lang="ts">
    import Overlay from "../../../components/Overlay.svelte";
    import { startQuiz } from "$lib/utils/api/quiz-apis";
    let promise: Promise<void>;
    let text = "test";
    const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
    const startQuizHandler = async () => {
        promise = startQuiz({
            quiz_type: "ValuTest",
        });
        await promise;
        window.location.href = "/ValuTest";
    };
</script>

<Overlay isTransparent={false} canBeExited={false}>
    <p class="text-xl mb-4">Welcome to the Values Test</p>
    <p>
        VALUTEST is a test that measures your accuracy in answering questions.
    </p>
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
