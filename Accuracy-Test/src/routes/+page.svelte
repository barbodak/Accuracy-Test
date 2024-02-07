<script lang="ts">
    import { goto } from "$app/navigation";
    import { retreiveAccount, retreiveQuiz } from "$lib/utils/api/quiz-apis";
    import { onMount } from "svelte";
    import Overlay from "../components/Overlay.svelte";
    let isAcuDone = false;
    let isValuDone = false;
    let hasValPerm = false;
    let hasAcuPerm = false;
    let acuAnswers = [0];
    let valuAnswers = [0];
    let first_name = "";
    let last_name = "";
    onMount(async () => {
        let account = await retreiveAccount().then((account) => {
            hasValPerm = account.valTest_permition;
            hasAcuPerm = account.acuTest_permition;
            first_name = account.first_name;
            last_name = account.last_name;
        });
        let valutest = await retreiveQuiz({ quiz_type: "ValuTest" }).then(
            (quiz) => {
                let now = new Date();
                let qdate = new Date(quiz.quiz_info);
                let delta = now.valueOf() - qdate.valueOf();
                if (Math.floor(delta / 1000) >= 5 * 60) isValuDone = true;
                valuAnswers = quiz.answers;
            }
        );
        let acutest = await retreiveQuiz({ quiz_type: "AcuTest" }).then(
            (quiz) => {
                let now = new Date();
                let qdate = new Date(quiz.quiz_info);
                let delta = now.valueOf() - qdate.valueOf();
                if (Math.floor(delta / 1000) >= 5 * 60) isAcuDone = true;
                acuAnswers = quiz.answers;
            }
        );
    });
</script>

<Overlay isTransparent={false} canBeExited={false}>
    <h1 class="text-xl">
        Welcome, {first_name}
        {last_name}
    </h1>
    <br />
    <br />
    <h1>
        {#if isAcuDone}
            <h1 class="text-l">you have already taken the AcuTest</h1>
            <!---->
            <!-- {#each acuAnswers as answer} -->
            <!--     {answer}, -->
            <!-- {/each} -->
        {:else if hasAcuPerm}
            <button
                class="bg-green-600 hover:bg-green-900 text-white font-bold py-2 px-4 rounded inline-block mt-2"
                on:click={() => {
                    goto("/AcuTest/start");
                }}
            >
                Start AcuTest</button
            >
        {:else}
            <p>You do not have permission to take the AcuTest</p>
        {/if}
    </h1>
    <br />
    <h1>
        {#if isValuDone}
            <h1>you have already taken the ValuTest</h1>
            <!-- {#each valuAnswers as answer} -->
            <!--     {answer}, -->
            <!-- {/each} -->
        {:else if hasValPerm}
            <button
                class="bg-green-600 hover:bg-green-900 text-white font-bold py-2 px-4 rounded inline-block mt-2"
                on:click={() => {
                    goto("/ValuTest/start");
                }}
            >
                Start ValuTest</button
            >
        {:else}
            <p>You do not have permission to take the ValuTest</p>
        {/if}
    </h1>
    <!-- {hasValPerm} -->
    <!-- {hasAcuPerm} -->
    <!-- {isAcuDone} -->
    <!-- {isValuDone} -->
</Overlay>
