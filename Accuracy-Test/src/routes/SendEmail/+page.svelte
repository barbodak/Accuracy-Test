<script lang="ts">
	let form = {
		url: '',
		email: '',
		name: '',
		title: '',
		body: ''
	};

	let sending = false;
	let resultMsg: string | null = null;
	let errorMsg: string | null = null;

	async function send() {
		resultMsg = null;
		errorMsg = null;
		sending = true;
		try {
			const res = await fetch('/api/send-pdf-email', {
				method: 'POST',
				headers: { 'content-type': 'application/json' },
				body: JSON.stringify(form)
			});
			if (!res.ok) {
				const text = await res.text();
				throw new Error(text || 'Request failed');
			}
			await res.json();
			resultMsg = 'Email request sent successfully.';
		} catch (e: any) {
			errorMsg = e?.message || 'Failed to send.';
		} finally {
			sending = false;
		}
	}
</script>

<div class="min-h-screen bg-slate-100 p-6">
	<div class="mx-auto max-w-xl rounded-lg bg-white p-6 shadow">
		<h1 class="mb-4 text-2xl font-bold text-slate-800">Send PDF Email</h1>

		<div class="space-y-4">
			<div>
				<label class="mb-1 block text-sm font-medium text-slate-700">Page URL to render</label>
				<input class="w-full rounded border p-2" bind:value={form.url} placeholder="https://your-site.com/ValuTest/result" />
			</div>
			<div>
				<label class="mb-1 block text-sm font-medium text-slate-700">Recipient Email</label>
				<input class="w-full rounded border p-2" bind:value={form.email} type="email" />
			</div>
			<div>
				<label class="mb-1 block text-sm font-medium text-slate-700">Name</label>
				<input class="w-full rounded border p-2" bind:value={form.name} />
			</div>
			<div>
				<label class="mb-1 block text-sm font-medium text-slate-700">Title</label>
				<input class="w-full rounded border p-2" bind:value={form.title} />
			</div>
			<div>
				<label class="mb-1 block text-sm font-medium text-slate-700">Body</label>
				<textarea class="w-full rounded border p-2" rows="5" bind:value={form.body} />
			</div>

			<button
				class="w-full rounded bg-indigo-600 px-4 py-2 font-semibold text-white hover:bg-indigo-700 disabled:opacity-60"
				on:click|preventDefault={send}
				disabled={sending}
			>
				{sending ? 'Sending…' : 'Send Email with PDF'}
			</button>

			{#if resultMsg}
				<p class="text-green-600">{resultMsg}</p>
			{/if}
			{#if errorMsg}
				<p class="text-red-600">{errorMsg}</p>
			{/if}
		</div>
	</div>
</div>
