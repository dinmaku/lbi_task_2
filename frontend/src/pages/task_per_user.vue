<template>
<div class="min-h-screen flex flex-col space-y-10 bg-gray-100 py-10 px-12 sm:px-6 lg:px-8 **font-mono** overflow-y-hidden">
  
  <div class="flex justify-between items-center">
    <div class="flex flex-col text-left space-y-1">
    <h1 class="text-3xl font-bold text-gray-800 font-sans">My Tasks</h1>
    <p class="font-semibold text-gray-500 text-md tracking-wide">Monitor all your tasks here</p>
     </div>  
    <form class="flex items-center w-[300px] mr-52">
              <label for="voice-search" class="sr-only">Search</label>
              <div class="relative w-full">
                <div class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none">
                  <svg aria-hidden="true" class="w-5 h-auto text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"></path>
                  </svg>
                </div>
                <input type="text" id="search-bar" class="bg-white border font-inter border-gray-400 text-gray-900 text-sm rounded-xl focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search here">
                <router-link to="/" class="flex absolute inset-y-0 right-0 items-center pr-3">
                  <svg aria-hidden="true" class="w-4 h-4 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  </svg>
                </router-link>
              </div>
        </form>
   </div>

   <!-- Alert Modal -->
    <div v-if="showAlert" class="fixed inset-0 bg-gray-800/20 overflow-y-auto flex justify-center items-center z-999">
      <div :class="['bg-white p-5 rounded-lg shadow-lg w-[400px] border-l-4', alertType === 'success' ? 'border-green-500' : 'border-red-500']">
        <div class="flex justify-between items-center mb-4">
          <h3 :class="['text-lg font-semibold', alertType === 'success' ? 'text-green-600' : 'text-red-600']">
            {{ alertType === 'success' ? 'Success' : 'Error' }}
          </h3>
        </div>
        <p class="text-gray-700">{{ alertMessage }}</p>
        <div class="flex justify-end mt-4">
          <button @click="closeAlert" class="px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 cursor-pointer">
            Close
          </button>
        </div>
      </div>
    </div>

    <div class="relative inline-block text-left">
        <label class="text-gray-700 font-semibold mr-2">Filter:</label>

        <select
            class="appearance-none bg-white text-gray-800 px-4 py-2 pr-8 rounded-lg border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-blue-400 cursor-pointer transition"
        >
            <option value="all">All Tasks</option>
            <option value="active">Active</option>
            <option value="completed">Completed</option>
            <option value="overdue">Overdue</option>
        </select>

        <!-- Dropdown arrow -->
        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
        </div>
        </div>


  <div class="relative shadow-md sm:rounded-xl w-full max-w-[1600px] h-[200] mt-2 font-inter mb-10">
    <div class="overflow-x-auto">
      <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400 mb-4 max-h-30 table-fixed">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th scope="col" class="w-16 px-2 py-3">#</th>
          <th scope="col" class="w-52 px-2 py-3">Task Name</th>
          <th scope="col" class="w-52 px-2 py-3">Type</th>
          <th scope="col" class="w-52 px-2 py-3">Assigned</th>
          <th scope="col" class="w-40 px-2 py-3">Deadline</th>
          <th scope="col" class="w-36 px-2 py-3">Status</th>
        </tr>
      </thead>
      <tbody>
        <tr
            v-for="(tasks, index) in paginatedTasks"
            :key="tasks.no"
            @click="showTaskModal(tasks)"
            class="border-b dark:border-gray-700 odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800
               hover:bg-gray-100 dark:hover:bg-gray-600 cursor-pointer transition duration-500 ease-in-out">
          <th scope="row" class="w-16 px-2 py-4 font-inter text-gray-900 whitespace-nowrap dark:text-white">{{tasks.dummyIndex }}</th>
          <td class="w-52 px-2 py-4 truncate">{{ tasks.title }}</td>
          <td class="w-52 px-2 py-4 truncate">{{ tasks.task_type_name }}</td>
            <td class="w-40 px-2 py-4">
              <div class="flex -space-x-2">
                <img
                  v-for="user in tasks.users"
                  :key="user.user_id"
                  :src="getUserAvatar(user)"
                  :alt="user.username"
                  class="w-10 h-10 rounded-full border-2 border-white hover:scale-110 transition"
                  :title="`${user.firstName} ${user.lastName}`"
                />
              </div>
            </td>
          <td class="w-36 px-2 py-4 truncate text-red-600">{{ formatDate(tasks.deadline) }}</td>
          <td
              class="w-36 px-2 py-4 truncate font-semibold capitalize"
              :class="{
                'text-blue-500': tasks.status === 'Pending',
                'text-yellow-500': tasks.status === 'In Progress',
                'text-green-500': tasks.status === 'Done',
                'text-red-500': tasks.status === 'Cancelled'
              }"
            >
              {{ tasks.status }}
            </td>
        </tr>
      </tbody>
    </table>

      <!-- Pagination Controls -->
      <div class="flex justify-center space-x-2 mt-4 mb-6">
        <button @click="prevTasksPage" :disabled="currentTasksPage === 1" 
            class="px-3 py-1 bg-[#27A9F5] text-white rounded-md hover:bg-[#0297F0] disabled:opacity-50 text-sm cursor-pointer">Previous</button>
        <button v-for="page in totalTasksPages" :key="page" @click="changeTasksPage(page)" 
            :class="{'bg-[#27A9F5]': currentTasksPage === page, 'bg-gray-300': currentTasksPage !== page}" 
            class="px-3 py-1 text-white rounded-md hover:bg-[#0297F0] text-xs cursor-pointer">
          {{ page }}
        </button>
        <button @click="nextTasksPage" :disabled="currentTasksPage === totalTasksPages" 
            class="px-3 py-1 bg-[#27A9F5] text-white rounded-md hover:bg-[#0297F0] disabled:opacity-50 text-xs cursor-pointer">Next</button>
      </div>
    </div>
  </div>


  <div
  v-if="taskModal"
  @click.self="taskModal = false"
  class="fixed inset-0 bg-gray-800/20 overflow-y-auto flex justify-center items-center z-[999]"
>
  <div class="bg-white p-6 rounded-xl shadow-2xl w-full max-w-xl mx-4">
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-800">Task Details</h2>
        <span class="text-sm text-white bg-blue-500 px-3 py-1 rounded-full">
          {{ taskDetails.task_type_name }}
        </span>
      </div>
      <hr class="border-gray-300" />

      <!-- Title & Description -->
      <div>
        <h3 class="text-3xl font-semibold text-gray-900 mb-2">
          {{ taskDetails.title }}
        </h3>
        <p class="text-gray-600 text-base">{{ taskDetails.description }}</p>
      </div>

      <!-- Status -->
      <div class="flex justify-center items-center gap-3">
        <p class="text-gray-600 font-semibold w-24">Status</p>
        <div
          class="flex items-center gap-2 cursor-pointer hover:bg-gray-100 px-2 py-1 rounded-md transition"
          @click="openStatusModal"
        >
          <span
            class="w-3 h-3 rounded-full"
            :class="{
              'bg-blue-500': taskDetails.status === 'Pending',
              'bg-yellow-500': taskDetails.status === 'In Progress',
              'bg-green-500': taskDetails.status === 'Done',
              'bg-red-500': taskDetails.status === 'Cancelled'
            }"
          ></span>
          <span class="text-gray-800 font-medium capitalize">
            {{ taskDetails.status }}
          </span>
        </div>
      </div>

      <!-- Assigned Users -->
      <div>
        <p class="text-gray-600 font-semibold mb-2">Assigned to:</p>
        <div class="flex flex-wrap gap-3">
          <div
            v-for="user in taskDetails.assigned_users"
            :key="user.user_id"
            class="flex items-center gap-2 bg-gray-100 px-3 py-1 rounded-full"
          >
            <img
              :src="getUserAvatar(user)"
              class="w-6 h-6 rounded-full border-2 border-white"
            />
            <span class="text-gray-800 font-medium">
              {{ user.firstName }} {{ user.lastName }}
            </span>
          </div>
        </div>
      </div>

      <!-- Dates -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <p class="text-gray-600 font-semibold">Start Date:</p>
          <p class="text-gray-900 font-medium">{{ taskDetails.created_at }}</p>
        </div>
        <div>
          <p class="text-gray-600 font-semibold">End Date:</p>
          <p class="text-gray-900 font-medium">{{ taskDetails.deadline }}</p>
        </div>


      </div>

      <!-- Actions -->
      <div class="flex justify-end">
        <button
          @click="taskModal = false"
          class="bg-gray-600 text-white px-5 py-2 rounded-lg hover:bg-gray-700 transition-transform transform hover:scale-105 cursor-pointer"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</div>

    <!-- Change Status Modal -->
    <div
      v-if="showStatusModal"
      @click.self="showStatusModal = false"
      class="fixed inset-0 bg-gray-800/40 flex justify-center items-center z-999"
    >
      <div class="bg-white rounded-lg shadow-lg w-[350px] p-6 space-y-5">
        <h2 class="text-xl font-semibold text-gray-800">Change Status</h2>

        <div class="space-y-2">
          <label
            v-for="option in statusOptions"
            :key="option"
            class="flex items-center space-x-2 cursor-pointer hover:bg-gray-100 p-2 rounded-md"
          >
            <input
              type="radio"
              name="status"
              :value="option"
              v-model="selectedStatus"
              class="text-blue-600 focus:ring-blue-500 cursor-pointer"
            />
            <span class="capitalize text-gray-700">{{ option }}</span>
          </label>
        </div>

        <div class="flex justify-end space-x-3">
          <button
            @click="showStatusModal = false"
            class="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 transition cursor-pointer"
          >
            Cancel
          </button>
          <button
            @click="updateStatus"
            class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition cursor-pointer"
          >
            Save
          </button>
        </div>
      </div>
    </div>

</div>

</template>

<script>
import axios from 'axios';

export default {
  name: 'TaskPerUser',
  data() {
    return {
      baseURL: 'http://127.0.0.1:5000',
      showAlert: false,
      alertMessage: '',
      alertType: 'success',
      currentTasksPage: 1,
      tasksPerPage: 10,
      tasks: [],
      taskModal: false,
      taskDetails: {
        task_id: null,
        title: '',
        description: '',
        status: '',
        created_at: '',
        deadline: '',
        task_type_id: null,
        task_type_name: '',
        assigned_user_ids: []
      },
      showStatusModal: false,
      selectedStatus: '',
      statusOptions: ['In Progress', 'Done',],

    };
  },
  computed: {
    filteredTasks() {
      return this.tasks || [];
    },
    totalTasksPages() {
      return Math.ceil(this.tasks.length / this.tasksPerPage);
    },
    paginatedTasks() {
      const start = (this.currentTasksPage - 1) * this.tasksPerPage;
      const end = start + this.tasksPerPage;
      return this.filteredTasks.map((task, index) => ({
            ...task,
            dummyIndex: start + index + 1
          })).slice(start, end);
    },
  },
  methods: {
    closeAlert() {
      this.showAlert = false;
    },
    showSuccess(message) {
      this.alertMessage = message;
      this.alertType = 'success';
      this.showAlert = true;
    },
    showError(message) {
      this.alertMessage = message;
      this.alertType = 'error';
      this.showAlert = true;
    },
    prevTasksPage() {
      if (this.currentTasksPage > 1) {
        this.currentTasksPage--;
      }
    },
    nextTasksPage() {
      if (this.currentTasksPage < this.totalTasksPages) {
        this.currentTasksPage++;
      }
    },
    changeTasksPage(page) {
      this.currentTasksPage = page;
    },
    showTaskModal(task) {
        this.taskModal = true;
        this.taskDetails = {
          task_id: task.task_id,
          title: task.title,
          description: task.description,
          status: task.status,
          created_at: this.formatDate(task.created_at),
          deadline: this.formatDate(task.deadline),
          task_type_id: task.task_type?.task_type_id || null,
          task_type_name: task.task_type?.task_type_name || '',
          // ✅ Keep full user objects instead of just IDs
          assigned_users: task.users || []
        };
      },
    
    async fetchTask(userId) {
        try {
          const token = sessionStorage.getItem('access_token');
          if (!token) {
            console.error('No token found');
            this.$router.push('/');
            return;
          }

          // ✅ Make sure you pass the real userId here
          const response = await axios.get(`${this.baseURL}/fetch_tasks_user/${userId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          });

          console.log('Raw API response:', response);

          if (response.status === 200 && Array.isArray(response.data)) {
            this.tasks = response.data;
            console.log('✅ Tasks fetched:', this.tasks);
          } else {
            console.warn('⚠️ Unexpected response format:', response.data);
            this.tasks = [];
          }
        } catch (error) {
          console.error('❌ Error fetching tasks:', error);
          this.tasks = [];
        }
      },

       getUserAvatar(user) {
            // Check if user has a preview (e.g., selected before saving)
            if (user.previewImage) {
              return user.previewImage;
            }

            // Use uploaded image if available
            const img = user.image;
            if (img && img.trim() !== '') {
              return img.startsWith('http')
                ? img
                : `http://localhost:5000/static/uploads/${img}`;
            }

            // Default placeholder
            return '/img/default_profile.png';
          },

          formatDate(dateString, format = 'long') {
              if (!dateString) return '';

              const date = new Date(dateString);

              if (isNaN(date)) return dateString; // fallback for invalid date

              const options =
                format === 'short'
                  ? { year: 'numeric', month: 'short', day: 'numeric' } // e.g. "Oct 20, 2025"
                  : { year: 'numeric', month: 'long', day: 'numeric' }; // e.g. "October 20, 2025"

              return date.toLocaleDateString('en-US', options);
            },

        openStatusModal() {
          this.selectedStatus = this.taskDetails.status;
          this.showStatusModal = true;
        },
        async updateStatus() {
          try {
            const response = await fetch(`http://localhost:5000/update_task_status/${this.taskDetails.task_id}`, {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({ status: this.selectedStatus }),
            });

            const result = await response.json();

            if (!response.ok) {
              throw new Error(result.error || 'Failed to update status');
            }

            // ✅ Update UI instantly
            this.taskDetails.status = this.selectedStatus;
            this.showStatusModal = false;
            await this.fetchTask(sessionStorage.getItem('user_id')); 
            console.log(result.message);
          } catch (error) {
            console.error('Error updating status:', error);
            alert('Failed to update status.');
          }
        },



  },
  mounted() {
    const userId = sessionStorage.getItem('user_id'); // or however you store it
        if (userId) {
          this.fetchTask(userId);
        }
  }
};


</script>

<style>

</style>