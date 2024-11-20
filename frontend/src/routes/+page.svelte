<script lang="ts">
	import {getToastStore} from '@skeletonlabs/skeleton';
	import type {ToastSettings} from "@skeletonlabs/skeleton";
	import bankingService, {type HistoryResponse} from "../services/banking";
	import Account from "../components/Account.svelte";
	import Transaction from "../components/Transaction.svelte";

	const toastStore = getToastStore();

	let balance: string = '0';
	let history: HistoryResponse[] = []
	let isLoadingBalance = false;
	let isLoadingHistory = false;

	async function getBalance() {
		try {
			isLoadingBalance = true;
			balance = (await bankingService.getBalance()).data.data.balance;
		}
		catch (e: any) {
			triggerErrorToast(e.message);
		}
		finally {
			isLoadingBalance = false;
		}
	}

	async function getHistory() {
		try {
			isLoadingHistory = true;
			history = (await bankingService.getHistory()).data.data;
		} catch (e: any) {
			triggerErrorToast(e.message);
		}
		finally {
			isLoadingHistory = false;
		}
	}

	function reloadAccount() {
		getBalance();
		getHistory();
	}

	function triggerErrorToast(message: string) {
		const toastSettings: ToastSettings = {
			message,
			timeout: 5000,
			background: 'variant-filled-error'
		}

		toastStore.trigger(toastSettings);
	}

	getBalance();
	getHistory();
</script>

<div class="mx-auto max-w-xl p-4">
	<div class="space-y-5 px-5 w-full">
		<h1 class="h1 text-center">HTTP Idempotence</h1>
		<Account balance={balance} history={history} isLoading={isLoadingBalance || isLoadingHistory} />
		<Transaction on:submitFinish={reloadAccount} />
	</div>
</div>
