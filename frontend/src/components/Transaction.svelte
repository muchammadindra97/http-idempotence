<script lang="ts">
    import {createEventDispatcher} from "svelte";
    import {getModalStore, getToastStore} from "@skeletonlabs/skeleton";
    import type {ModalSettings, ToastSettings} from "@skeletonlabs/skeleton";
    import banking from "../services/banking";

    const dispatch = createEventDispatcher();
    const modalStore = getModalStore();
    const toastStore = getToastStore();

    let mode = 'deposit';
    let isSimulateError = false;
    let idempotenceKey = generateRandomString();
    let amount = '0';
    let isSubmitting = false;

    function generateRandomString() {
        return Math.random().toString(32).substring(2);
    }

    function resetForm() {
        mode = 'deposit';
        isSimulateError = false;
        idempotenceKey = generateRandomString();
        amount = '0';
    }

    async function submitTransaction() {
        try {
            isSubmitting = true;

            if (mode === 'deposit') {
                await banking.deposit(amount, idempotenceKey);
            } else {
                await banking.withdraw(amount, idempotenceKey);
            }


            if (isSimulateError) {
                const modal: ModalSettings = {
                    type: 'alert',
                    title: 'Error!',
                    body: 'Simulated error, data is saved (check account table). Re-submit to see Idempotence error or click reset to clear.',
                    buttonTextCancel: 'Close'
                };
                modalStore.trigger(modal);
                isSimulateError = false;
            }
            else {
                resetForm();
            }

            dispatch('submitFinish', true);
        } catch (e: any) {
            const toastSettings: ToastSettings = {
                message: e.message,
                timeout: 5000,
                background: 'variant-filled-error'
            }

            toastStore.trigger(toastSettings);
        } finally {
            isSubmitting = false;
        }
    }
</script>

<form class="card" on:submit="{submitTransaction}">
    <header class="card-header p-4"><h2 class="h3">Transaction</h2></header>
    <hr />
    <section class="p-4 space-y-4">
        <div class="grid grid-cols-3 gap-3">
            <div>
                Mode
            </div>
            <div class="col-span-2 flex items-center gap-8">
                <div class="flex items-center space-x-2">
                    <input bind:group={mode} class="radio" type="radio" name="mode" value="deposit" />
                    <p>Deposit</p>
                </div>
                <div class="flex items-center space-x-2">
                    <input bind:group={mode} class="radio" type="radio" name="mode" value="withdraw" />
                    <p>Withdraw</p>
                </div>
            </div>
        </div>
        <div class="grid grid-cols-3 gap-3">
            <div>
                Simulate Error
            </div>
            <div class="col-span-2">
                <div class="flex items-center space-x-2">
                    <input class="checkbox" type="checkbox" bind:checked="{isSimulateError}" />
                    <p>Yes</p>
                </div>
            </div>
        </div>
        <div class="grid grid-cols-3 gap-3">
            <div>Idempotence Key</div>
            <div class="col-span-2">
                {idempotenceKey}
            </div>
        </div>
        <div>
            <input bind:value={amount} class="input text-end" type="number" placeholder="Amount" min="0" />
        </div>
        <div class="flex items-center justify-center space-x-2">
            <button on:click={resetForm} type="button" class="btn variant-filled w-28" disabled="{isSubmitting}">Reset</button>
            <button type="submit" class="btn variant-filled w-28" disabled="{isSubmitting || amount <= '0'}">Submit</button>
        </div>
    </section>
</form>