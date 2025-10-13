<template>
  <div class="w-screen h-screen flex overflow-hidden font-inter">
    <!-- Sidebar -->
    <div class="w-[250px] h-full bg-gray-200 text-center text-white top-0 left-0 overflow-y-hidden">
      <div class="h-[70px] bg-gray-200 flex justify-center items-center">
        <div class="flex text-center items-center px-[20px]">
          <h3 class="font-bold text-2xl text-gray-800">LBI</h3>
        </div>
      </div>
      <div class="h-[calc(100vh-50px)] bg-[#4A90E2] py-[20px]">
        <div class="flex flex-col justify-between h-full px-[20px] space-y-[10px]">
        <div class = "flex flex-col space-y-[10px]">
          <router-link
            to="/dashboard"
            class="inline-flex items-center py-[20px] px-[10px] w-full text-md font-interBold font-semibold rounded-md border-gray-200 hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group whitespace-nowrap"
          >
            <img
            aria-hidden="true"
            class="mr-2 w-[30px] h-[30px] transition duration-300 ease-in-out group-hover:brightness-0"
            src="../assets/icons/dashboard.png"
            />
            Dashboard
          </router-link>
          <router-link
            to="/manage-users"
            class="inline-flex items-center py-[20px] px-[10px] w-full text-md font-interBold font-semibold rounded-md border-gray-200 hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group whitespace-nowrap"
          >
            <img
            aria-hidden="true"
            class="mr-2 w-[30px] h-[30px] transition duration-300 ease-in-out group-hover:brightness-0"
            src="../assets/icons/manage_users.png"
            />
            Manage Users
          </router-link>
          
          </div>
            <button
                @click="showLogoutConfirmModal"
                class="inline-flex items-center py-[15px] px-[10px] w-full text-md font-interBold font-semibold rounded-md border-gray-200 hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group whitespace-nowrap cursor-pointer">
                <img aria-hidden="true" class="mr-2 w-[20px] h-[20px] text-white transition duration-300 ease-in-out group-hover:brightness-0"
                 src="../assets/icons/logout.png">
                Log out
            </button>

        </div>
      </div>
    </div>

    <!-- Headbar + Content -->
    <div class="w-full h-full bg-[#50E3C2] text-center">
      <div class="h-[70px] bg-gray-100 flex items-center shadow-xl px-[20px] w-full py-[10px] z-10 shadow-md">
        <div class="w-full flex justify-center">
          <!-- Optional: Add title/logo here -->
        </div>
      </div>

      <!-- Router view (main content area) -->
      <div class="min-h-[calc(100vh-50px)] h-full bg-[#F7FDFF] overflow-y-auto">
        <router-view />
      </div>
      <!-- Status Confirmation Modal -->
        <div v-if="logoutModal" @click.self="closeLogoutConfirmModal" class="fixed inset-0 bg-gray-800/40 overflow-y-auto flex justify-center items-center z-50">
          <div class="bg-gray-100 p-5 rounded-lg shadow-lg w-[400px]">
            <div class="flex flex-col items-center">
              <h2 class="text-xl font-semibold mb-4">Logout</h2>
              <p class="mb-6 text-center">Are you sure you want to logout?</p>
              <div class="flex space-x-4">             
                <button 
                  @click="closeLogoutConfirmModal" 
                  class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-opacity-90 transform-transition duration-300 transform hover:scale-105 cursor-pointer">
                  Cancel
                </button>
                <button 
                  @click="logout" 
                  class = "w-20 h-10 bg-blue-500 text-gray-100 font-semibold rounded-lg shadow-md  transform-transition duration-300 transform hover:scale-105 cursor-pointer">
                  Yes
                </button>
              </div>
            </div>
          </div>
        </div>

    </div>
    
  </div>


  
</template>

<script>
export default {
  name: 'DefaultLayout',
  data() {
    return {
      logoutModal: false,

    };
  },
  methods: {
    showLogoutConfirmModal() {
      this.logoutModal = true;
    },
    closeLogoutConfirmModal() {
      this.logoutModal = false;
    },
    logout() {
      localStorage.removeItem('authToken');
      this.$router.push('/');
    },
  },
};
</script>

<style scoped>
html {
  scroll-behavior: smooth;
}
</style>