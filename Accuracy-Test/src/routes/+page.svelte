<script lang="ts">
    import { goto } from "$app/navigation";
    import { startQuiz } from "$lib/utils/api/quiz-apis";
    let promise: Promise<void>;
    const startQuizHandler = async () => {
        promise = startQuiz({
            quiz_type: "AcuTest",
            test: "1",
        });
        await promise;
        goto("/AcuTest");
    };
</script>

<h1>Hello World</h1>
<button class="p-3 m-3 bg-red-500" on:click={startQuizHandler}
    >start quiz</button
>
<svg width="3000" height="1000">
    <defs>
        <marker
            id="arrow"
            markerWidth="13"
            markerHeight="13"
            refy="6"
            orient="auto"
        >
            <path d="M2,2 L2,11 L10,6 L2,2" style="fill:red;" />
        </marker>
    </defs>

    <path
        d="M30,150 L100,50"
        style="stroke:red; stroke-width: 1.25px; fill: none;
        marker-end: url(#arrow);"
    />
</svg>
