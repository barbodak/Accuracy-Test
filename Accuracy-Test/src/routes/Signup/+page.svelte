<script lang="ts">
    import { goto } from "$app/navigation";
    import { signup } from "$lib/utils/api/authentication";

    // This holds the data we will send to the backend
    let formData = {
        first_name: "",
        last_name: "",
        email: "",
        university: "",
        degree: "",
        major: "",
        age: null as number | null,
        sex: "", // Will be 'M', 'F', or 'O'
    };

    let error: string | null = null; // To display submission errors
    let submitPromise: Promise<any>; // For the async button

    $: {
        if (formData.degree === "diploma") {
            formData.university = "diploma";
            formData.major = "diploma";
        } else {
            if (formData.university === "diploma") {
                formData.university = "";
            }
            if (formData.major === "diploma") {
                formData.major = "";
            }
        }
    }

    async function handleSubmit() {
        // Simple validation
        if (
            !formData.first_name ||
            !formData.last_name ||
            !formData.age ||
            !formData.sex ||
            !formData.email ||
            !formData.university || // This will be 'diploma' if Diploma is selected
            !formData.degree ||
            !formData.major // This will be 'diploma' if Diploma is selected
        ) {
            error = "لطفا تمام فیلدها را پر کنید.";
            return;
        }
        if (formData.age <= 0) {
            error = "لطفا سن معتبری وارد کنید.";
            return;
        }
        error = null;

        // Call the finalize API
        // Assign the promise to the outer variable to trigger the {#await} block
        submitPromise = signup(formData);

        try {
            await submitPromise; // Wait for the promise to resolve
            // Success! Redirect to the dashboard.
            await goto("/ValuTest/start"); // <-- Or wherever your main app is
        } catch (e) {
            console.error("Failed to Signup:", e);
            error = "خطایی رخ داد. لطفا دوباره تلاش کنید.";
        }
    }
</script>

<svelte:head>
    <title>تکمیل پروفایل</title>
    <style>
        body {
            /* Matches the background from your login +page.svelte */
            background-color: #f1f5f9; /* Slate 100 */
        }
    </style>
</svelte:head>

<div
    class="flex min-h-screen items-center justify-center bg-slate-100 p-4"
    dir="rtl"
>
    <form
        class="w-full max-w-lg space-y-6 rounded-lg bg-white p-8 shadow-lg"
        on:submit|preventDefault={handleSubmit}
    >
        <div class="flex justify-center">
            <img
                src="/images/metasan-logo-fa.svg"
                alt="Metasan Logo"
                class="h-12 w-auto"
            />
        </div>

        <h2 class="text-center text-2xl font-bold text-slate-800">
            تکمیل پروفایل
        </h2>

        <div>
            <label
                for="first_name"
                class="mb-1 block text-sm font-medium text-slate-700"
            >
                نام
            </label>
            <input
                type="text"
                name="first_name"
                id="first_name"
                bind:value={formData.first_name}
                class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                placeholder="مثلا: سارا"
                required
            />
        </div>

        <div>
            <label
                for="last_name"
                class="mb-1 block text-sm font-medium text-slate-700"
            >
                نام خانوادگی
            </label>
            <input
                type="text"
                name="last_name"
                id="last_name"
                bind:value={formData.last_name}
                class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                placeholder="مثلا: رضایی"
                required
            />
        </div>

        <div>
            <label
                for="age"
                class="mb-1 block text-sm font-medium text-slate-700"
            >
                سن
            </label>
            <input
                type="number"
                name="age"
                id="age"
                min="1"
                bind:value={formData.age}
                class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                placeholder="۲۵"
                required
            />
        </div>

        <div>
            <label
                for="sex"
                class="mb-1 block text-sm font-medium text-slate-700"
            >
                جنسیت
            </label>
            <select
                name="sex"
                id="sex"
                bind:value={formData.sex}
                class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                required
            >
                <option value="" disabled>لطفا انتخاب کنید...</option>
                <option value="M">مرد</option>
                <option value="F">زن</option>
                <!-- <option value="O">سایر</option> -->
            </select>
        </div>

        <div>
            <label
                for="email"
                class="mb-1 block text-sm font-medium text-slate-700"
            >
                ایمیل
            </label>
            <input
                type="email"
                name="email"
                id="email"
                bind:value={formData.email}
                class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                placeholder="you@gmail.com"
                required
            />
        </div>

        <div>
            <label
                for="degree"
                class="mb-1 block text-sm font-medium text-slate-700"
            >
                مقطع تحصیلی
            </label>
            <select
                name="degree"
                id="degree"
                bind:value={formData.degree}
                class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                required
            >
                <option value="" disabled>لطفا انتخاب کنید...</option>
                <option value="diploma">دیپلوم</option>
                <option value="bachelor">کارشناسی</option>
                <option value="masters">کارشناسی ارشد</option>
                <option value="doctorate">دکترا</option>
            </select>
        </div>

        {#if formData.degree && formData.degree !== "diploma"}
            <div>
                <label
                    for="university"
                    class="mb-1 block text-sm font-medium text-slate-700"
                >
                    دانشگاه
                </label>
                <input
                    type="text"
                    name="university"
                    id="university"
                    bind:value={formData.university}
                    class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                    placeholder="دانشگاه شریف"
                    required
                />
            </div>

            <div>
                <label
                    for="major"
                    class="mb-1 block text-sm font-medium text-slate-700"
                >
                    رشته تحصیلی
                </label>
                <input
                    type="text"
                    name="major"
                    id="major"
                    bind:value={formData.major}
                    class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                    placeholder="مهندسی کامپیوتر"
                    required
                />
            </div>
        {/if}

        {#if error}
            <div
                class="rounded-md border border-red-300 bg-red-50 p-3 text-sm text-red-700"
            >
                {error}
            </div>
        {/if}

        {#await submitPromise}
            <button
                type="submit"
                disabled
                class="flex w-full justify-center rounded-lg bg-indigo-400 px-4 py-2.5 text-sm font-medium text-white opacity-75 shadow-sm"
            >
                در حال ذخیره...
            </button>
        {:then}
            <button
                type="submit"
                class="flex w-full justify-center rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white shadow-sm transition-colors duration-200 hover:bg-indigo-700 focus:outline-none focus:ring-4 focus:ring-indigo-300"
            >
                ذخیره و ادامه
            </button>
        {:catch error}
            <button
                type="submit"
                class="flex w-full justify-center rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white shadow-sm transition-colors duration-200 hover:bg-indigo-700 focus:outline-none focus:ring-4 focus:ring-indigo-300"
            >
                ذخیره و ادامه
            </button>
        {/await}
    </form>
</div>
