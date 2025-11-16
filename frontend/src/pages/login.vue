<template>

<section class="bg-[#3284E3] dark:bg-gray-900">
  <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
      
      <div class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
          <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
              <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                  Log in to your account
              </h1>
              <form class="space-y-4 md:space-y-6" @submit.prevent="handleLogin">
                  <div>
                     <p class="text-sm text-red-600" v-if="errorMessage"> {{ errorMessage }}</p>
                      <label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your email</label>
                      <input type="email" name="email" v-model="email" placeholder="admin@gmail.com" class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required="">
                  </div>
                  <div>
                      <label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Password</label>
                      <input type="password" name="password" v-model="password" placeholder="••••••••" class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required="">
                  </div>
                  <div class="flex items-center justify-between">
                      <div class="flex items-center">
                        <input
                          id="remember"
                          type="checkbox"
                          v-model="rememberMe"
                          class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <div class="ml-3 text-sm">
                          <label for="remember" class="text-gray-500 dark:text-gray-300">
                            Remember me
                          </label>
                        </div>
                      </div>
                      <a href="#" class="text-sm font-medium text-primary-600 hover:underline dark:text-primary-500">Forgot password?</a>
                  </div>
                  <button type="submit" class="w-full text-white bg-gray-800 hover:bg-gray-900 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800 my-5 cursor-pointer">Log in</button>
              </form>
          </div>
      </div>
  </div>
</section>

</template>

<script>
import axios from 'axios'

axios.defaults.withCredentials = true

export default {
  name: 'AdminLogin',
  data() {
    return {
      email: '',
      password: '',
      errorMessage: '',
      rememberMe: false,
    };
  },
  methods: {
    async handleLogin() {
        try {

           // Log the request
            console.log('Sending login request with:', {
                email: this.email,
                password: '***'
            });

          const response = await axios.post('http://127.0.0.1:5000/login', {
            email: this.email,
            password: this.password,
          });

          if (response.data.message === "Login successful") {
            const access_token = response.data.access_token;
            const userProfile = response.data.user;

            // Store token based on "Remember me"
            if (this.rememberMe) {
              localStorage.setItem('access_token', access_token);
            } else {
              sessionStorage.setItem('access_token', access_token);
            }

            // Store user profile
            if (response.data.user) {
              const userProfile = response.data.user;
              localStorage.setItem('user_id', userProfile.user_id) || sessionStorage.setItem('user_id', userProfile.user_id);
              localStorage.setItem('email', userProfile.email) || sessionStorage.setItem('email', userProfile.email);
              localStorage.setItem('user_type', userProfile.user_type);
              localStorage.setItem('access_token', access_token);
              sessionStorage.setItem('firstName', userProfile.firstName);
              sessionStorage.setItem('lastName', userProfile.lastName);
              console.log('Stored user profile:', userProfile);
            }

            localStorage.setItem('loggedIn', 'true');

            this.$emit('loginSuccess');

          
            if (userProfile.user_type === 'admin' || userProfile.user_type === 'client') {
              this.$router.push('/projects');
            } else {
              this.$router.push('/task-per-user');
            }

            } else {
              this.errorMessage = 'Unexpected response from server.';
            }

        } catch (error) {
          if (error.response && error.response.data) {
            this.errorMessage = error.response.data.error || 'Login failed. Please check your credentials.';
          } else {
            this.errorMessage = 'An error occurred. Please try again later.';
          }
          console.error('Login error:', error);
        }
      },


    resetLoginForm() {
      this.email = '';
      this.password = '';
      this.errorMessage = '';
    },
    

  },

  mounted() {
    const token =
    localStorage.getItem('access_token') ||
    sessionStorage.getItem('access_token');
   }
}
</script>



<style scoped>

</style>