<script lang="ts">
	import '../app.postcss';
    import { initializeStores, Modal, Toast } from '@skeletonlabs/skeleton';

    initializeStores();
</script>

<Modal />
<Toast />
<slot />
