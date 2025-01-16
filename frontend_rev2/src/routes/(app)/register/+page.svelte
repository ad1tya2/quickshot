<!-- YOU CAN DELETE EVERYTHING IN THIS PAGE -->
<script>
	import axios from 'axios';
	import { writable } from 'svelte/store'
	import { onMount } from 'svelte'


	const jwt = writable('')

	let email = '';
	let username = '';
	let password = '';

	async function hash(string) {
		const utf8 = new TextEncoder().encode(string);
		const hashBuffer = await crypto.subtle.digest('SHA-256', utf8);
		const hashArray = Array.from(new Uint8Array(hashBuffer));
		const hashHex = hashArray.map((bytes) => bytes.toString(16).padStart(2, '0')).join('');
		return hashHex;
	}

	async function register() {
		try {
			const response = await axios.get('http://api.mossdaddy.tech/register', {
				params: {
					email: email,
					username: username,
					password: await hash(password)
				}
			});

			if (response.data.jwt) {
				localStorage.setItem('jwt', response.data.jwt);
				window.location.href='/user/dashboard'
                jwt.set(response.data.jwt);
			} else {
				console.error(response.data.message);
			}
		} catch (error) {
			if (
				error.response &&
				error.response.status === 401 &&
				error.response.data.message === 'User already exists'
			) {
				alert(error.response.data.message);
			}
		}
	}
	onMount(async () => {
		if (typeof localStorage !== 'undefined') {
            const storedJWT = localStorage.getItem('jwt');
            if (storedJWT) {
                jwt.set(storedJWT);
				window.location.href = '/user/dashboard';
            }
        }
    });
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Register</h2>
		<form class="login-form">
			<label class="label">
				<span>Email</span>
				<br />
				<input
					bind:value={email}
					class="input variant-form-material"
					type="email"
					placeholder="example@gmail.com"
				/>
			</label>
			<br />
			<label class="label">
				<span>Username</span>
				<br />
				<input
					bind:value={username}
					class="input variant-form-material"
					type="text"
					placeholder="Username"
				/>
			</label>
			<br />
			<label class="label">
				<span>Password</span>
				<br />
				<input
					bind:value={password}
					class="input variant-form-material"
					type="password"
					placeholder="Password"
				/>
			</label>
			<br />
			<button on:click={register} type="submit" class="btn variant-filled">Register</button>
		</form>
		<a href="/login" class="text-primary-400">Already have an account? Login</a> 
	</div>
</div>

<style lang="postcss">
	.login-form {
		background-color: #2c3656;
		border-radius: 25px;
		width: 30vw;
		padding: 30px;
		height: 43vh;
	}
</style>
