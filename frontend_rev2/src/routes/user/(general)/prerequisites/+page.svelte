<script>
	import { api } from '$lib/apiMiddleWare.js';
	import { Stepper, Step, SlideToggle } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
	let images = [];
	let uploaded_files_images = [];
	function handleFileUploadImages(event) {
		const files = event.target.files;
		for (let i = 0; i < files.length; i++) {
			const file = files[i];
			console.log('File:', file);
			console.log('Images:', images);
			if (uploaded_files_images.includes(file)) {
				continue;
			}
			uploaded_files_images.push(file);
			const reader = new FileReader();
			reader.onload = (e) => {
				const image = e.target.result;
				if (!images.includes(e.target.result)) {
					images = [...images, image];
				}
			};
			reader.readAsDataURL(file);
		}
	}

	function handleDragOverImages(event) {
		event.preventDefault();
	}

	function handleDropImages(event) {
		event.preventDefault();
		const files = event.dataTransfer.files;
		for (let i = 0; i < files.length; i++) {
			const file = files[i];
			const reader = new FileReader();
			if (uploaded_files_images.includes(file)) {
				continue;
			}
			uploaded_files_images.push(file);
			reader.onload = (e) => {
				const image = e.target.result;
				if (!images.includes(e.target.result)) {
					images = [...images, image];
				}
			};
			reader.readAsDataURL(file);
		}
	}

	async function handleSubmitImages(event) {
		event.preventDefault();
		const formData = new FormData(event.target);
		const files = uploaded_files_images;
		console.log('Files:', files);

		for (const file of files) {
			formData.append('files', file);
		}

		try {
			const response = await api.post('/user/upload', formData, {
				headers: {
					'Content-Type': 'multipart/form-data'
				}
			});
			if (response.status != 200) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const responseData = await response.data;
			console.log('Response:', responseData);
		} catch (error) {
			console.error('Error:', error);
		}
	}

	let audios = [];
	let uploaded_files_audios = [];
	function handleFileUploadAudios(event) {
		const files = event.target.files;
		for (let i = 0; i < files.length; i++) {
			const file = files[i];
			console.log('File:', file);
			console.log('audios:', audios);
			if (uploaded_files_audios.includes(file)) {
				continue;
			}
			uploaded_files_audios.push(file);
			const reader = new FileReader();
			reader.onload = (e) => {
				const audio = e.target.result;
				if (!audios.includes(e.target.result)) {
					audios = [...audios, audio];
				}
			};
			reader.readAsDataURL(file);
		}
	}

	function handleDragOverAudios(event) {
		event.preventDefault();
	}

	function handleDropAudios(event) {
		event.preventDefault();
		const files = event.dataTransfer.files;
		for (let i = 0; i < files.length; i++) {
			const file = files[i];
			const reader = new FileReader();
			if (uploaded_files_audios.includes(file)) {
				continue;
			}
			uploaded_files_audios.push(file);
			reader.onload = (e) => {
				const audio = e.target.result;
				if (!audios.includes(e.target.result)) {
					audios = [...audios, audio];
				}
			};
			reader.readAsDataURL(file);
		}
	}

	async function handleSubmitAudios(event) {
		event.preventDefault();
		const formData = new FormData(event.target);
		const files = formData.getAll('audios');
		console.log('Files:', files);

		for (const file of files) {
			formData.append('files', file);
		}

		try {
			const response = await api.post('/user/upload', formData, {
				headers: {
					'Content-Type': 'multipart/form-data'
				}
			});
			if (response.status != 200) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const responseData = await response.data;
			console.log('Response:', responseData);
		} catch (error) {
			console.error('Error:', error);
		}
	}
    let locked = true;
    let unlocked = false;
    function changeLock() {
        locked = !locked;
        unlocked = !unlocked;
    }

    function onCompleteHandler() {
        window.location.href= '/user/editor';
    }
</script>

<div class="stepper">
	<Stepper on:complete={onCompleteHandler}>
		<Step>
			<svelte:fragment slot="header">Checklist</svelte:fragment>
			Make sure you have all the media required.
		</Step>
		<Step>
			<svelte:fragment slot="header">Images</svelte:fragment>
			Upload extra images:
			<div
				class="upload-container"
				on:dragover={handleDragOverImages}
				on:drop={handleDropImages}
				role="button"
				tabindex="0"
			>
				<p>Drag and drop your files here</p>
				<br />

				<form
					on:submit={handleSubmitImages}
					style="display:flex; flex-direction:column; justify-content: center; align-items:center"
				>
					<input
						type="file"
						id="images"
						name="images"
						class="hidden"
						multiple
						accept="image/*"
						on:change={handleFileUploadImages}
					/>

					<button type="button" class="btn variant-filled"
						><label for="images">Select Images</label></button
					>
					<br />

					<div class="uploaded-images">
						{#each images as image}
							<img class="uploaded-image" src={image} alt="hi" />
						{/each}
					</div>

					<input type="submit" value="Upload" class="upload-button" />
				</form>
			</div>
		</Step>
		<Step>
			<div
				class="upload-container"
				on:dragover={handleDragOverAudios}
				on:drop={handleDropAudios}
				role="button"
				tabindex="0"
			>
				<p>Drag and drop your files here</p>
				<br />
				<form
					on:submit={handleSubmitAudios}
					style="display:flex; flex-direction:column; justify-content: center; align-items:center"
				>
					<input
						type="file"
						id="audios"
						name="audios"
						class="hidden"
						multiple
						accept="audio/*"
						on:change={handleFileUploadAudios}
					/>

					<button type="button" class="btn variant-filled"
						><label for="audios">Select Custom Audio Files</label></button
					>
					<br />

					<div class="uploaded-audios">
						{#each audios as audio, i}
							<div class="uploaded-audio">
								<audio controls>
									<source src={audio} type="audio/mpeg" />
									Your browser does not support the audio element.
								</audio>
								<p id="filename">{uploaded_files_audios[i].name}</p>
							</div>
						{/each}
					</div>

					<input type="submit" value="Upload" class="upload-button" />
				</form>
			</div>
		</Step>
		<Step {locked}>
			<svelte:fragment slot="header">Final Step.</svelte:fragment>
			<p>Are you sure you have added all required media?</p>
			<aside class="alert variant-ghost-warning">
				<div class="alert-message">
					<p>Confirmed?</p>
				</div>
				<div class="alert-actions">
					<SlideToggle
						name="locked-state"
						bind:checked={unlocked}
						on:click={changeLock}
						active="bg-warning-500"
					/>
				</div>
			</aside>
		</Step>
	</Stepper>
</div>

<style lang="postcss">
	.stepper {
		margin-left: 10px;
		margin-right: 10px;
		justify-content: center;
		align-items: center;
	}
	.upload-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		margin-top: 10px;
		margin-left: 10%;
		margin-right: 10%;
		border: 2px dashed #ccc;
		padding: 20px;
		padding-top: 30px;
	}

	.uploaded-images {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		margin-top: 20px;
	}

	.uploaded-image {
		width: 200px;
		height: 200px;
		margin: 10px;
		object-fit: cover;
	}

	.upload-button {
		margin-top: 10px;
		padding: 10px 20px;
		border: none;
		border-radius: 5px;
		background-color: #333333;
		color: #ffffff;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}

	.uploaded-audios {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
		margin-top: 20px;
	}

	.uploaded-audio {
		margin: 10px;
		object-fit: cover;
	}
	#filename {
		max-width: 300px;
		text-overflow: ellipsis;
	}
</style>
