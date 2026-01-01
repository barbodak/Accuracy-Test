<script lang="ts">
    import { goto } from "$app/navigation";
    import { signup } from "$lib/utils/api/authentication";

    // This holds the data we will send to the backend
    let formData = {
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        university: "u",
        degree: "",
        major: "m",
        age: null as number | null,
        sex: "", // Will be 'M', 'F', or 'O'
    };

    let error: string | null = null; // To display submission errors
    let submitPromise: Promise<any>; // For the async button

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
        if (formData.phone) {
            const phoneRegex = /^09\d{9}$/; // Starts with 09, followed by 8 digits
            if (!phoneRegex.test(formData.phone)) {
                error = "شماره تلفن نامعتبر";
                return;
            }
        }
        error = null;

        // Call the finalize API
        // Assign the promise to the outer variable to trigger the {#await} block
        submitPromise = signup(formData);

        try {
            await submitPromise; // Wait for the promise to resolve
            // Success! Redirect to the dashboard.
            await goto("/AcuTest/Text/start"); // <-- Or wherever your main app is
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
            <!-- fill heare with a good looking text for the top of a signup page -->
        </div>
        <div class="mb-8 flex flex-col items-center text-center">
            <div
                class="mb-3 flex h-16 w-16 items-center justify-center rounded-full bg-indigo-100 text-indigo-600"
            >
                <!-- Simple User Icon SVG -->
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="h-8 w-8"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"
                    />
                </svg>
            </div>
            <h1 class="text-2xl font-bold text-slate-800">
                تکمیل اطلاعات کاربری
            </h1>
            <p class="mt-2 text-sm text-slate-500">
                برای شروع آزمون، لطفاً مشخصات فردی و تحصیلی خود را وارد کنید.
            </p>
        </div>

        <!-- <h2 class="text-center text-2xl font-bold text-slate-800"> -->
        <!--     تکمیل پروفایل -->
        <!-- </h2> -->

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
                autocomplete="off"
                bind:value={formData.first_name}
                class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                placeholder="نام به زبان فارسی"
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
                autocomplete="off"
                bind:value={formData.last_name}
                class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                placeholder="نام خانوادگی به زبان فارسی"
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
                autocomplete="off"
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
                autocomplete="off"
                bind:value={formData.email}
                class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                placeholder="you@gmail.com"
                required
            />
        </div>

        <div>
            <label
                for="phone"
                class="mb-1 block text-sm font-medium text-slate-700"
            >
                شماره تماس (درصورت تمایل)
            </label>
            <input
                type="phoen"
                name="phone"
                id="phone"
                autocomplete="off"
                bind:value={formData.phone}
                class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                placeholder="۰۹۱۲۳۴۵۶۷۸۹"
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
                <option value="diploma">دیپلم</option>
                <option value="student">دانشجو</option>
                <option value="bachelor">کارشناسی</option>
                <option value="masters">کارشناسی ارشد</option>
                <option value="doctorate">دکترا</option>
            </select>
        </div>

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
