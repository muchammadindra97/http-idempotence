<script lang="ts">
    import { ProgressRadial } from '@skeletonlabs/skeleton';
    import type {HistoryResponse} from "../services/banking";

    export let balance: string;
    export let history: HistoryResponse[];
    export let isLoading: boolean;

</script>

<div class="card">
    <header class="card-header p-4"><h2 class="h3">Account</h2></header>
    <hr />
    <section class="p-4 space-y-3">
        {#if !isLoading}
            <div class="flex justify-between items-center">
                <div>Balance</div>
                <p class="h1">{balance}</p>
            </div>

            <div class="table-container overflow-auto" style="height: 300px">
                <table class="table table-hover">
                    <thead>
                    <tr>
                        <th class="text-center">Id</th>
                        <th class="text-center">Action</th>
                        <th class="text-center">Amount</th>
                        <th class="text-center">Time</th>
                    </tr>
                    </thead>
                    <tbody>
                    {#each history as row, i}
                        <tr>
                            <td class="text-center">{row.id}</td>
                            <td class="text-center">{row.action}</td>
                            <td class="text-end">{row.amount}</td>
                            <td class="text-center">{row.time}</td>
                        </tr>
                    {/each}
                    </tbody>
                </table>
            </div>
        {:else}
            <div class="flex justify-center items-center p-4" style="height: 348px">
                <ProgressRadial />
            </div>
        {/if}
    </section>
</div>