<template>
  <div class="min-h-screen bg-gray-100 py-10 px-12 sm:px-6 lg:px-8 **font-mono** overflow-y-hidden">
    <div class="flex flex-row items-center space-x-20">
    <h1 class="text-3xl font-bold tracking-wide text-gray-800 font-sans">Daily Task</h1>
    <form class="flex items-center w-[300px]">
              <label for="voice-search" class="sr-only">Search</label>
              <div class="relative w-full">
                <div class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none">
                  <svg aria-hidden="true" class="w-5 h-auto text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"></path>
                  </svg>
                </div>
                <input type="text" id="search-bar" class="bg-white border font-inter border-gray-400 text-gray-900 text-sm rounded-xl focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search here" required v-model="searchAccount">
                <router-link to="/" class="flex absolute inset-y-0 right-0 items-center pr-3">
                  <svg aria-hidden="true" class="w-4 h-4 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  </svg>
                </router-link>
              </div>
        </form>
   </div>
   <div class="flex h-screen flex-row justify-start mt-10 space-x-20">
     <div class="flex flex-col text-start space-y-2 overflow-y-auto scroll-hidden">
          <label for="" class="text-2xl font-semibold py-5 text-gray-600">Project Summary</label>
            <div class="flex flex-row">
              <div class="w-[300px] h-[150px] bg-green-50 rounded-lg shadow-md p-5 mr-10 space-y-2">
                <p class="text-gray-500 font-semibold">Total Projects Done</p>
                <h2 class="text-4xl font-bold mt-3">12</h2>
                <p class="text-sm text-gray-400"><span class="text-green-600">2.5%</span> More than last month</p>
              </div>
              <div class="w-[300px] h-[150px] bg-orange-50 rounded-lg shadow-md p-5 mr-10 space-y-2">
                <p class="text-gray-500 font-semibold">Ongoing Projects</p>
                <h2 class="text-4xl font-bold mt-3">8</h2>
                <p class="text-sm text-gray-400"><span class="text-green-600">1.5%</span> More than last month</p>
              </div>
              <div class="w-[300px] h-[150px] bg-purple-100 rounded-lg shadow-md p-5 space-y-2">
                <p class="text-gray-500 font-semibold">Completed Projects</p>
                <h2 class="text-4xl font-bold mt-3">4</h2>
                <p class="text-sm text-gray-400"><span class="text-green-600">5.5%</span> More than last month</p>
              </div>
            </div>
          <div class="flex flex row mt-5 space-x-10">
              <div class="flex justify-between items-center w-[300px] h-[60px] bg-gray-400/80 rounded-xl shadow-md p-5">
                 <h1 class="text-white text-xl font-semibold">Coming Next</h1>
                 <div class="rounded-full bg-white w-8 h-8 mr-2">
                  <p class="text-gray-500 text-xl font-semibold text-center">3</p>
                 </div>
              </div>
              <div class="flex justify-between items-center w-[300px] h-[60px] bg-blue-400/80 rounded-xl shadow-md p-5">
                 <h1 class="text-white text-xl font-semibold">In Progress</h1>
                 <div class="rounded-full bg-white w-8 h-8 mr-2">
                  <p class="text-gray-500 text-xl font-semibold text-center">5</p>
                 </div>
              </div>
              <div class="flex justify-between items-center w-[300px] h-[60px] bg-green-600/80 rounded-xl shadow-md p-5">
                 <h1 class="text-white text-xl font-semibold">Completed</h1>
                 <div class="rounded-full bg-white w-8 h-8 mr-2">
                  <p class="text-gray-500 text-xl font-semibold text-center">3  </p>
                 </div>
              </div>
                 
          </div>

        <div class="grid grid-cols-3 gap-10 mt-10">
           <div v-for="(card, index) in cardInfo" :key="index" class="w-[300px] h-[320px] bg-white border border-gray-300 rounded-lg shadow-md p-5 
           transition-transform duration-300 transform hover:scale-105 cursor-pointer" @click="">
               <div class="h-9 w-22 bg-red-100 rounded-full mb-4 flex items-center justify-center">
                 <span class="text-red-600 text-xs font-semibold">{{ card.task_type }}</span >
               </div>
              <h2 class="text-lg font-semibold mb-4">{{ card.title }}</h2>
              <p class="text-gray-600 line-clamp-3 w-64">{{ card.description }}</p>
              <p class="text-blue-600 font-semibold mt-2">{{ card.status }}</p>
              <p class="text-gray-600 text-sm font-semibold mt-5">Created at: <span class="text-gray-900">{{ card.create_at }}</span></p>
              <hr class ="my-5 border-gray-300">
              <div class="flex justify-between items-center">
                <div class="flex items-center">
                  <img src="/img/default_profile.png" alt="Avatar" class="w-8 h-8 rounded-full mr-2">
                  
            </div>
          </div>
         
          

     </div> 
   </div>
     
    
  </div>

      <div class="flex flex-col text-start space-y-2 overflow-y-hidden">
        <label for="" class="text-2xl font-semibold py-5 text-gray-600">Create a new task</label>
        <div class="bg-gray-200/70 w-[550px] h-[620px] rounded-xl shadow-md p-10">
          <div class="flex flex-col space-y-2">
             <label for="" class="font-semibold text-lg text-gray-700">Title</label>
             <input type="text" class="w-2/3 h-10 border-b border-gray-400 outline-none" placeholder="Enter a comprehensive task title">
             <label for="" class="font-semibold text-lg text-gray-700 mt-3">Task type </label>
               <div class="grid grid-cols-4 gap-y-2">
                 <button v-for="(type, index) in taskType" :key="index" class="rounded-full w-28 h-8 flex justify-center items-center cursor-pointer" :class="getColorClass(type.title)">
                      <p class="text-sm text-white font-semibold">{{ type.title }}</p>
                 </button>
                <button @click="showAddTaskType" class="ml-1 h-8 w-8 bg-gray-300 rounded-full flex justify-center items-center cursor-pointer translate-transform duration-300 transform hover:scale-110">
                  <span class="text-2xl font-semibold leading-none mb-[5px]">+</span>
                </button>
               </div>
              <label for="" class="font-semibold text-lg text-gray-700 mt-3">Description</label>
              <textarea name="" id="" class="w-2/3 h-30 bg-white border-none rounded-lg shadow-md outline-none p-3" placeholder="Enter a task description"></textarea>

              <label for="" class="font-semibold text-lg text-gray-700 mt-3">Assign to</label>
               <select class="w-2/3 h-10 bg-white rounded-lg shadow-md text-md font-semibold outline-none cursor-pointer appearance-none p-2">
                 <option value="" disabled selected class="text-gray-500 text-semibold">Select a user</option>
                 <option value="" >John Doe</option>
                 <option value="" >Pedro Penduko</option>
                 <option value="" >Katrina Lim</option>
                 <option value="" >Chris Gulpan</option>
               </select>

               <div class="flex justify-center items-center mt-5">
                  <button class="bg-blue-400 text-center text-lg font-semibold h-10 w-full rounded-lg
                   shadow-md cursor-pointer translate-transform duration-300 transform hover:scale-105">Create Task</button>
            </div>
          </div>

          
         
          
        </div>    
      </div>
  </div>
 
       
        <div v-if="AddTaskType" @click.self="closeAddTaskType" class="fixed inset-0 bg-gray-800/30 overflow-y-auto flex justify-center items-center z-100">
          <div class="bg-white p-5 rounded-lg shadow-lg w-[400px]">
            <div class="flex flex-col items-center space-y-8">
              <h2 class="text-xl font-semibold mb-4">Add New Task Type</h2>
               <input type="text" class="w-3/4 h-10 rounded-lg shadow-md p-2 border-none bg-gray-100" placeholder="Enter task type">
              <div class="flex space-x-4">             
                <button 
                  @click="closeAddTaskType" 
                  class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-opacity-90 cursor-pointer transfomr-transition duration-300 transform hover:scale-105">
                  Cancel
                </button>
                <button 
                  @click="confirmStatusChange" 
                  class = "w-20 h-10 bg-blue-500 text-gray-100 font-semibold rounded-lg shadow-md cursor-pointer transform-transition duration-300 transform hover:scale-105">
                  Save
                </button>
              </div>
            </div>
          </div>
        </div>
  
 

  </div>
</template>

<script>

export default {
  name: 'Dashboard',
  data() {
    return {
      cardInfo: [],
      taskType: [
        {title: 'Bug'},
        {title: 'UI Design'},
        {title: 'Improvement'},
        {title: 'Data Entry'},
        {title: 'Feature'},
      ],
      AddTaskType: false,
    };
  },
  methods: {
     loadDummyCards() {
      this.cardInfo = [
        {
          task_type: 'Bug',
          title: 'Fix login issue',
          description: 'Users cannot log in with correct credentials.',
          status: 'Open',
          create_at: '2025-10-17 09:00'
        },
        {
          task_type: 'Feature',
          title: 'Add dark mode',
          description: 'Implement dark mode toggle for dashboard.',
          status: 'In Progress',
          create_at: '2025-10-16 14:30'
        },
        {
          task_type: 'Improvement',
          title: 'Optimize image loading',
          description: 'Compress and lazy-load dashboard images.',
          status: 'Completed',
          create_at: '2025-10-15 11:45'
        },
        {
          task_type: 'Bug',
          title: 'Fix sidebar collapse',
          description: 'Sidebar does not collapse on mobile view.',
          status: 'Open',
          create_at: '2025-10-14 08:20'
        },
        {
          task_type: 'Feature',
          title: 'Add user roles',
          description: 'Implement role-based access control.',
          status: 'In Progress',
          create_at: '2025-10-13 10:00'
        },
        {
          task_type: 'Improvement',
          title: 'Improve search speed',
          description: 'Optimize backend queries for faster search.',
          status: 'Completed',
          create_at: '2025-10-12 13:15'
        },
        {
          task_type: 'Bug',
          title: 'Fix notification badge',
          description: 'Badge count does not update in real-time.',
          status: 'Open',
          create_at: '2025-10-11 16:45'
        },
        {
          task_type: 'Feature',
          title: 'Add export to CSV',
          description: 'Allow users to export data tables to CSV.',
          status: 'In Progress',
          create_at: '2025-10-10 09:30'
        },
        {
          task_type: 'Improvement',
          title: 'Refactor auth module',
          description: 'Clean up and modularize authentication logic.',
          status: 'Completed',
          create_at: '2025-10-09 12:00'
        },
        {
          task_type: 'Bug',
          title: 'Fix avatar upload',
          description: 'Image upload fails for large files.',
          status: 'Open',
          create_at: '2025-10-08 15:10'
        }
      ]
    },

   getColorClass(title) {
      switch (title) {
        case 'Bug':
          return 'bg-blue-800 focus:outline focus:outline-2 focus:outline-blue-700';
        case 'UI Design':
          return 'bg-red-500 focus:outline focus:outline-2 focus:outline-red-700';
        case 'Improvement':
          return 'bg-purple-500 focus:outline focus:outline-2 focus:outline-purple-700';
        case 'Data Entry':
          return 'bg-yellow-500 focus:outline focus:outline-2 focus:outline-yellow-700'
        case 'Feature':
          return 'bg-orange-500 focus:outline focus:outline-2 focus:outline-orange-700'
        default:
          return 'bg-gray-500 focus:outline focus:outline-2 focus:outline-blue-500'; // optional fallback
      }
    },
    showAddTaskType() {
      this.AddTaskType = true;
    },

    closeAddTaskType()
    {
      this.AddTaskType = false;
    },

  
    },
  mounted() {
    this.loadDummyCards();
   }
  }
</script>
<style>
/* In your CSS file */
.scroll-hidden::-webkit-scrollbar {
  display: none;
}
.scroll-hidden {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}</style>
