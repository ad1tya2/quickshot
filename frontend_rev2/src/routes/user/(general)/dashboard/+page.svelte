<script>
    import { onMount } from 'svelte';
	import { getDecoded, api } from '$lib/apiMiddleWare.js';
	function isImage(media) {
		return media.mediatype == 'image';
	}
	
	onMount(async () => {
		console.log(getDecoded());
		let medias = getDecoded().paths;
		console.log(medias);
		let tasks = [];
		let t = 0;
		async function imgadd() {
			if (t >= medias.length) {
				return;
			}
			let image = medias[t];
			if (isImage(image)) {
				let i = (
					await api.get(`/getfile/${image.filename}`, {
						responseType: 'blob'
					})
				).data;
				var uri = URL.createObjectURL(i);
				var img = new Image();
				img.className = 'photo';
				img.style.objectFit = 'cover';
				img.style.transition = 'transform 0.3s ease';

				// Add event listener for mouse enter
				img.addEventListener("mouseenter", function() {
					// Modify the transform property to scale up
					img.style.transform = "scale(1.05)";
				});

				// Add event listener for mouse leave
				img.addEventListener("mouseleave", function() {
					// Reset the transform property to its original state
					img.style.transform = "scale(1)";
				});

				img.src = uri;
				document.getElementById('photo-grid').appendChild(img);
			}
			t++;
			imgadd();
		}
		imgadd();
	});
</script>

<div class="flex flex-wrap" style="margin-bottom: 19.35vw;">
	<div class="w-full mb-12 xl:mb-0 px-4" style="margin: 10vw;">
		<div id="photo-grid"></div>
	</div>
</div>

<style>
	#photo-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
		grid-gap: 10px;
	}
</style>