<script>
	import { getDrawerStore } from '@skeletonlabs/skeleton';

	const drawerStore = getDrawerStore();

	function drawerClose() {
		drawerStore.close();
	}
</script>

<nav class="list-nav p-4">
	<ul>
		<li><a href="/user/dashboard" on:click={drawerClose}>Dashboard</a></li>
		<li><a href="/user/upload_images" on:click={drawerClose}>Upload Images</a></li>
		<li><a href="/user/upload_audio" on:click={drawerClose}>Upload Audio</a></li>
		<li><a href="/user/prerequisites" on:click={drawerClose}>Video Editor</a></li>
	</ul>
</nav>
