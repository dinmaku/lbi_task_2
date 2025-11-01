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
            v-if="isAdmin"
            active-class="bg-white text-gray-900 whitespace-nowrap"
            class="inline-flex items-center py-[20px] px-[10px] w-full text-md font-interBold font-semibold rounded-md border-gray-200 hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group whitespace-nowrap"
          >
            <img
            aria-hidden="true"
            class="mr-2 w-[30px] h-[30px] transition duration-300 ease-in-out"
            :class="{'brightness-0': isActive('/dashboard'),
                      'group-hover:brightness-0': true

            }"
            src="../assets/icons/dashboard.png"
            />
            Dashboard
          </router-link>
          <router-link
            to="/manage-users"
            v-if="isAdmin"
            active-class="bg-white text-gray-900 whitespace-nowrap"
            class="inline-flex items-center py-[20px] px-[10px] w-full text-md font-interBold font-semibold rounded-md border-gray-200 hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group whitespace-nowrap"
          >
            <img
            aria-hidden="true"
            class="mr-2 w-[30px] h-[30px] transition duration-300 ease-in-out"
            :class="{'brightness-0': isActive('/manage-users'),
                      'group-hover:brightness-0': true

            }"
            src="../assets/icons/manage_users.png"
            />
            Manage Users
          </router-link>
          <router-link
            to="/task-per-user"
            active-class="bg-white text-gray-900 whitespace-nowrap"
            class="inline-flex items-center py-[20px] px-[10px] w-full text-md font-interBold font-semibold rounded-md border-gray-200 hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group whitespace-nowrap"
          >
            <img
            aria-hidden="true"
            class="mr-2 w-[30px] h-[30px] transition duration-300 ease-in-out"
            :class="{'brightness-0': isActive('/task-per-user'),
                      'group-hover:brightness-0': true

            }"
            src="../assets/icons/task.png"
            />
            My Tasks
          </router-link>
          <router-link
            to="/update-profile"
            active-class="bg-white text-gray-900 whitespace-nowrap"
            class="inline-flex items-center py-[20px] px-[10px] w-full text-md font-interBold font-semibold rounded-md border-gray-200 hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group whitespace-nowrap"
          >
            <img
            aria-hidden="true"
            class="mr-2 w-[30px] h-[30px] transition duration-300 ease-in-out"
            :class="{'brightness-0': isActive('/update-profile'),
                      'group-hover:brightness-0': true

            }"
            src="../assets/icons/settings.png"
            />
            Settings
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

    <!-- Main Content Area -->
    <div class="w-full h-full bg-[#50E3C2] text-center relative">
      
      <!-- Router view (main content area) -->
      <div class="min-h-[calc(100vh-50px)] h-full bg-[#F7FDFF] overflow-y-auto">
        <router-view />
      </div>

      <!-- Chat Icon -->
      <div
        @click="toggleChat"
        class="fixed bottom-6 right-6 bg-blue-600 hover:bg-blue-700 text-white rounded-full w-14 h-14 flex items-center justify-center shadow-lg cursor-pointer z-50"
      >
        💬
      </div>

      <!-- Chat Window -->
      <div
        v-if="chatOpen"
        class="fixed bottom-24 right-6 w-[350px] bg-white rounded-lg shadow-lg border border-gray-200 flex flex-col z-50"
      >
        <!-- Header -->
        <div class="bg-blue-600 text-white px-4 py-2 rounded-t-lg flex justify-between items-center">
          <h3 class="font-semibold text-lg">Chat</h3>
          <button @click="chatOpen = false" class="text-white text-xl hover:text-gray-200">&times;</button>
        </div>

        <!-- Users List -->
        <div v-if="!selectedUser" class="flex-1 overflow-y-auto max-h-[400px] p-3">
          <p class="text-gray-500 text-sm mb-2">Select a user to start chatting:</p>
          <div
            v-for="user in users"
            :key="user.id"
            @click="selectUser(user)"
            class="flex items-center p-2 mb-2 bg-gray-50 rounded-md hover:bg-blue-100 cursor-pointer"
          >
            <img :src="user.avatar || '/img/default_profile.png'" class="w-10 h-10 rounded-full mr-3" />
            <div>
              <p class="font-medium text-gray-700">{{ user.name }}</p>
              <p class="text-xs text-gray-400">{{ user.email }}</p>
            </div>
          </div>
        </div>

        <!-- Chat Messages -->
        <div v-else class="flex flex-col h-[400px]">
          <div class="flex items-center justify-between px-4 py-2 border-b">
            <div class="flex items-center">
              <img :src="selectedUser.avatar || '/img/default_profile.png'" class="w-8 h-8 rounded-full mr-2" />
              <span class="font-semibold text-gray-700">{{ selectedUser.name }}</span>
            </div>
            <button @click="selectedUser = null" class="text-gray-500 hover:text-gray-700 text-sm">← Back</button>
          </div>

          <div class="flex-1 overflow-y-auto p-3 bg-gray-50">
            <div
              v-for="msg in messages"
              :key="msg.id"
              class="mb-2"
              :class="msg.fromSelf ? 'text-right' : 'text-left'"
            >
              <span
                :class="msg.fromSelf
                  ? 'inline-block bg-blue-600 text-white px-3 py-2 rounded-lg'
                  : 'inline-block bg-gray-200 text-gray-800 px-3 py-2 rounded-lg'"
              >
                {{ msg.text }}
              </span>
            </div>
          </div>

          <div class="flex items-center p-2 border-t">
            <input
              v-model="newMessage"
              @keyup.enter="sendMessage"
              type="text"
              placeholder="Type a message..."
              class="flex-1 px-3 py-2 text-sm border rounded-md outline-none"
            />
            <button
              @click="sendMessage"
              class="ml-2 bg-blue-600 text-white px-3 py-2 rounded-md hover:bg-blue-700 text-sm"
            >
              Send
            </button>
          </div>
        </div>
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
import ManageUsers from './manage_users.vue';


export default {
  name: 'DefaultLayout',
  components: {
    ManageUsers,
  },
  data() {
    return {
      logoutModal: false,
      chatOpen: false,
      selectedUser: null,
      newMessage: "",
      messages: [],
      users: [
        { id: 1, name: "John Doe", email: "john@example.com", avatar: "" },
        { id: 2, name: "Jane Smith", email: "jane@example.com", avatar: "" },
        { id: 3, name: "Admin User", email: "admin@example.com", avatar: "" },
      ],

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
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_type');
      sessionStorage.removeItem('access_token');
      this.$router.push('/');
    },
    isActive(route) {
      return this.$route.path === route;
    },
     toggleChat() {
      this.chatOpen = !this.chatOpen;
    },
    selectUser(user) {
      this.selectedUser = user;
      this.messages = [
        { id: 1, text: "Hey there!", fromSelf: false },
        { id: 2, text: "Hello! How are you?", fromSelf: true },
      ];
    },
    sendMessage() {
      if (!this.newMessage.trim()) return;
      this.messages.push({
        id: Date.now(),
        text: this.newMessage,
        fromSelf: true,
      });
      this.newMessage = "";
    },
  },
  computed: {
    isAdmin() {
      return localStorage.getItem('user_type') === 'admin';
    }
  }
};
</script>

<style scoped>
html {
  scroll-behavior: smooth;
}
</style>