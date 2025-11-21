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
                <input type="text" id="search-bar" class="bg-white border font-inter border-gray-400 text-gray-900 text-sm rounded-xl focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search here">
                <router-link to="/" class="flex absolute inset-y-0 right-0 items-center pr-3">
                  <svg aria-hidden="true" class="w-4 h-4 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  </svg>
                </router-link>
              </div>
        </form>
   </div>
   <div class="flex h-screen flex-row justify-start mt-10 space-x-20">
     <div class="flex flex-col text-start space-y-2 overflow-y-auto scroll-hidden">
          <label for="" class="text-2xl font-semibold py-5 text-gray-600">Task Summary</label>
            <div class="flex flex-row">
              <div class="w-[300px] h-[150px] bg-green-50 rounded-lg shadow-md p-5 mr-10 space-y-2">
                <p class="text-gray-500 font-semibold">Total Tasks Done</p>
                <h2 class="text-4xl font-bold mt-3">{{ stats?.done?.count || 0 }}</h2>
                <p class="text-sm text-gray-400"><span class="text-green-600">{{ stats.done.growth >= 0 ? '+' : '' }}{{ stats.done.growth }}%</span> 
                 {{ stats.done.growth >= 0 ? 'More' : 'Less' }} than last month </p>
              </div>
              <div class="w-[300px] h-[150px] bg-orange-50 rounded-lg shadow-md p-5 mr-10 space-y-2">
                <p class="text-gray-500 font-semibold">Ongoing Tasks</p>
                <h2 class="text-4xl font-bold mt-3">{{ stats.ongoing.count || 0 }}</h2>
                <p class="text-sm text-gray-400"><span class="text-green-600">{{ stats.ongoing.growth >= 0 ? '+' : '' }}{{ stats.ongoing.growth }}%</span>
                  {{ stats.ongoing.growth >= 0 ? 'More' : 'Less' }} than last month</p>
              </div>
              <div class="w-[300px] h-[150px] bg-red-100 rounded-lg shadow-md p-5 space-y-2">
                <p class="text-gray-500 font-semibold">Cancelled Tasks</p>
                <h2 class="text-4xl font-bold mt-3">{{ stats.cancelled.count || 0 }}</h2>
                <p class="text-sm text-gray-400"><span class="text-green-600">{{ stats.cancelled.growth >= 0 ? '+' : '' }}{{ stats.cancelled.growth }}%</span>
                   {{ stats.cancelled.growth >= 0 ? 'More' : 'Less' }} than last month</p>
              </div>
            </div>
          <div class="flex flex row mt-5 space-x-10">
              <div class="flex justify-between items-center w-[300px] h-[60px] bg-gray-400/80 rounded-xl shadow-md p-5">
                 <h1 class="text-white text-xl font-semibold">Coming Next</h1>
                 <div class="rounded-full bg-white w-8 h-8 mr-2">
                  <p class="text-gray-500 text-xl font-semibold text-center">{{ pendingTasksCount() }}</p>
                 </div>
              </div>
              <div class="flex justify-between items-center w-[300px] h-[60px] bg-blue-400/80 rounded-xl shadow-md p-5">
                 <h1 class="text-white text-xl font-semibold">In Progress</h1>
                 <div class="rounded-full bg-white w-8 h-8 mr-2">
                  <p class="text-gray-500 text-xl font-semibold text-center">{{ inProgressTasksCount() }}</p>
                 </div>
              </div>
              <div class="flex justify-between items-center w-[300px] h-[60px] bg-green-600/80 rounded-xl shadow-md p-5">
                 <h1 class="text-white text-xl font-semibold">Completed</h1>
                 <div class="rounded-full bg-white w-8 h-8 mr-2">
                  <p class="text-gray-500 text-xl font-semibold text-center">{{ doneTasksCount() }}</p>
                 </div>
              </div>
                 
          </div>

        <div class="grid grid-cols-3 gap-10 mt-10">
            <div
              v-for="(card, index) in cardInfo"
              :key="card.task_id"
              @click="showEditTaskForm(card)"
              class="w-[300px] h-auto bg-white border border-gray-300 rounded-lg shadow-md p-5 transition-transform duration-300 transform hover:scale-105 cursor-pointer"
              
            >
              <div class="h-9 w-22 bg-red-100 rounded-full mb-4 flex items-center justify-center">
                <span class="text-red-600 text-xs font-semibold">
                  {{ card.task_type.task_type_name }}
                </span>
              </div>
              <h2 class="text-lg font-semibold mb-4">{{ card.title }}</h2>
              <p class="text-gray-600 line-clamp-2 w-64">{{ card.description }}</p>
              <p class="text-blue-600 font-semibold mt-2"
                :class="{'text-blue-600' : card.status === 'Pending',
                          'text-yellow-600' : card.status === 'In Progress',
                          'text-green-600' : card.status === 'Done',
                          'text-red-600' : card.status === 'Cancelled'
                }">{{ card.status }}</p>
              <p class="text-gray-600 text-sm font-semibold mt-5">
                Created at: <span class="text-green-600">{{ formatDate(card.created_at) }}</span>
              </p>
              <p class="text-gray-600 text-sm font-semibold mt-5">
                Deadline: <span class="text-red-600">{{ formatDate(card.deadline) }}</span>
              </p>
              <hr class="my-5 border-gray-300" />
              <div class="flex justify-between items-center">
                <div class="flex items-center">
                  <div
                    v-for="user in card.users"
                    :key="user.user_id"
                    class="relative group"
                  >
                    <img
                      :src="getUserAvatar(user)"
                      :alt="user.firstName"
                      class="w-8 h-8 rounded-full mr-2"
                      :title="user.firstName + ' ' + user.lastName"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          
    
  </div>

      <form @submit.prevent="createTask" class="flex flex-col text-start space-y-2 overflow-y-hidden">
          <label for="" class="text-2xl font-semibold py-5 text-gray-600">Create a new task</label>
          <div class="bg-gray-200/70 w-[550px] h-[700px] rounded-xl shadow-md p-10">
            <div class="flex flex-col space-y-2">
              <label for="" class="font-semibold text-lg text-gray-700">Title</label>
              <input
                type="text"
                class="w-2/3 h-10 border-b border-gray-400 outline-none"
                placeholder="Enter a comprehensive task title"
                v-model="title"
              />

              <label for="" class="font-semibold text-lg text-gray-700 mt-3">Task type</label>
              <div class="grid grid-cols-4 gap-3">
                <button
                  v-for="(type, index) in taskTypes"
                  :key="type.task_type_id || index"
                  @click="selectTaskType(type)"
                  type="button"
                  class="rounded-full w-28 h-8 flex justify-center items-center cursor-pointer transition-transform duration-300 transform hover:scale-105"
                  :class="[
                    getColorClass(type.task_type_name),
                    selectedTaskType === type.task_type_id ? 'ring-2 ring-offset-2 ring-blue scale-105' : 'opacity-90'
                  ]"
                >
                  <p class="text-sm text-white font-semibold truncate">
                    {{ type.task_type_name }}
                  </p>
                </button>

                <!-- Add button -->
                <button
                  type="button"
                  @click="showAddTaskType"
                  class="h-8 w-8 bg-gray-300 rounded-full flex justify-center items-center cursor-pointer transition-transform duration-300 transform hover:scale-110"
                >
                  <span class="text-2xl font-semibold leading-none mb-[7px]">+</span>
                </button>
              </div>

              <label for="" class="font-semibold text-lg text-gray-700 mt-3">Description</label>
              <textarea
                name=""
                id=""
                class="w-2/3 h-30 bg-white border-none rounded-lg shadow-md outline-none p-3"
                placeholder="Enter a task description"
                v-model="description"
              ></textarea>

              <!-- Assign Section -->
               <div class = "flex flex-row items-center space-x-2">
              <label class="font-semibold text-lg text-gray-700 mt-3">Assigned to</label>
              <button
                  @click="openAssignModal"
                  type="button"
                  class="h-6 w-6 bg-gray-300 rounded-full flex justify-center items-center cursor-pointer transition-transform duration-300 transform hover:scale-110 mt-3"
                >
                  <span class="text-2xl font-semibold leading-none mb-[7px]">+</span>
                </button>
              </div>
              <div class="flex -space-x-3 mb-3">
                <div
                  v-for="userId in selectedUserIds"
                  :key="userId"
                  class="relative group"
                >
                  <img
                    :src="getUserAvatar(users.find(u => u.user_id === userId))"
                    :alt="getUserName(userId)"
                    class="w-10 h-10 rounded-full border-2 border-white shadow-md cursor-pointer transition-transform duration-300 hover:scale-110"
                    :title="getUserName(userId)"
                  />
                </div>
              </div>

             <label class="font-semibold text-lg text-gray-700 mt-3">Deadline</label>
              <input
                type="date"
                id="date"
                name="date"
                v-model="deadline"
                class="block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />

        
              <div class="flex justify-center items-center mt-5">
                <button
                  type="submit"
                  class="bg-blue-400 text-center text-lg font-semibold h-10 w-full rounded-lg shadow-md cursor-pointer translate-transform duration-300 transform hover:scale-105"
                >
                  Create Task
                </button>
              </div>
            </div>
          </div>
        </form>
  </div>
  
 
       
        <div v-if="AddTaskTypeForm" @click.self="closeAddTaskType" class="fixed inset-0 bg-gray-800/30 overflow-y-auto flex justify-center items-center z-50">
          <div class="bg-white p-5 rounded-lg shadow-lg w-[400px]">
            <div class="flex flex-col items-center space-y-8">
              <h2 class="text-xl font-semibold mb-4">Add New Task Type</h2>
               <input v-model="newTaskTypeName" type="text" class="w-3/4 h-10 rounded-lg shadow-md p-2 border-none bg-gray-100" placeholder="Enter task type">
              <div class="flex space-x-4">             
                <button 
                  @click="closeAddTaskType" 
                  class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-opacity-90 cursor-pointer transfomr-transition duration-300 transform hover:scale-105">
                  Cancel
                </button>
                <button 
                  @click.prevent="addTaskType"
                  class = "w-20 h-10 bg-blue-500 text-gray-100 font-semibold rounded-lg shadow-md cursor-pointer transform-transition duration-300 transform hover:scale-105">
                  Save
                </button>
              </div>
            </div>
          </div>
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

    <!-- Assign Task Modal -->
      <div
        v-if="showAssignModal"
        @click.self="closeAssignModal"
        class="fixed inset-0 bg-gray-800/40 flex justify-center items-center z-50"
      >
        <div class="bg-white rounded-lg shadow-lg w-[450px] p-6 space-y-5">
          <h2 class="text-xl font-semibold text-gray-800">Assign Task</h2>

          <p class="text-sm text-gray-500 mb-2">
            Select users for: <span class="font-semibold">{{ title || 'New Task' }}</span>
          </p>

          <!-- User list -->
          <div class="max-h-60 overflow-y-auto border rounded-lg p-3 space-y-2">
            <div
              v-for="user in users"
              :key="user.user_id"
              class="flex items-center space-x-2"
            >
              <input
                type="checkbox"
                :id="'user-' + user.user_id"
                :value="user.user_id"
                v-model="selectedUserIds"
                class="cursor-pointer w-4 h-4 text-blue-600 border-gray-300 rounded"
              />
              <label :for="'user-' + user.user_id" class="cursor-pointer text-gray-700">
                {{ user.firstName }} {{ user.lastName }}
              </label>
            </div>
          </div>

          <!-- Buttons -->
          <div class="flex justify-end space-x-3 mt-4">
            <button
              @click="closeAssignModal"
              class="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 transition cursor-pointer"
            >
              Cancel
            </button>
            <button
              @click="confirmAssignUsers"
              class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition cursor-pointer"
            >
              Assign
            </button>
          </div>
        </div>
      </div>



  <!---Edit Task Modal-->
    <form @submit.prevent="updateTask" v-if="editTaskForm" @click.self="closeEditTaskForm" class = "fixed inset-0 bg-gray-800/20 overflow-y-auto flex justify-center items-center z-99">
         <div class="bg-white w-[1100px] h-[780px] rounded-md flex p-3">
          <div class="flex justify-between items-center gap-x-10 w-full">
          <div class="flex flex-col mt-3">
          <div class="flex justify-between items-center px-7">
           <h1 class = "text-2xl font-semibold py-5 text-gray-600">Update Task</h1>
            <!-- Status -->
          <div class="flex justify-center items-center gap-3">
            <div
              class="flex items-center gap-2 cursor-pointer hover:bg-gray-100 px-2 py-1 rounded-md transition"
              @click="openStatusModal"
            >
              <span
                class="w-3 h-3 rounded-full"
                :class="{
                  'bg-blue-500': editTaskData.status === 'Pending',
                  'bg-yellow-500': editTaskData.status === 'In Progress',
                  'bg-green-500': editTaskData.status === 'Done',
                  'bg-red-500': editTaskData.status === 'Cancelled'
                }"
              ></span>
              <span class="text-gray-800 font-medium capitalize">
                {{ editTaskData.status }}
              </span>
            </div>
          </div>

           </div>
            <div class="flex flex-col space-y-2 p-10">
              <label for="" class="font-semibold text-start text-lg text-gray-700">Title</label>
              <input
                type="text"
                class="w-2/3 h-10 border-b border-gray-400 outline-none"
                placeholder="Enter a comprehensive task title"
                v-model="editTaskData.title"
              />

              <label for="" class="font-semibold text-start text-lg text-gray-700 mt-5">Task type</label>
               <div class="grid grid-cols-4 gap-2 mt-1">
              <button
                  v-for="(type, index) in taskTypes"
                  :key="type.task_type_id || index"
                  @click="selectTaskType(type)"
                  type="button"
                  class="rounded-full w-28 h-8 flex justify-center items-center cursor-pointer transition-transform duration-300 transform hover:scale-105"
                  :class="[
                    getColorClass(type.task_type_name),
                    editTaskData.task_type_id === type.task_type_id ? 'ring-2 ring-offset-2 ring-blue scale-105' : 'opacity-90'
                  ]"
                >
                  <p class="text-sm text-white font-semibold truncate">
                    {{ type.task_type_name }}
                  </p>
                </button>
                </div>

              <label for="" class="font-semibold text-start text-lg text-gray-700 mt-3">Description</label>
              <textarea
                name=""
                id=""
                class="w-full h-30 bg-gray-100 border-none rounded-lg shadow-md outline-none p-3"
                placeholder="Enter a task description"
                v-model="editTaskData.description"
              ></textarea>
              <div class="flex flex-row items-center space-x-2 mt-3">
              <label for="" class="font-semibold text-start text-lg text-gray-700">Assigned to</label>
              <button
                  @click="openEditAssignModal"
                  type="button"
                  class="h-6 w-6 bg-gray-300 rounded-full flex justify-center items-center cursor-pointer transition-transform duration-300 transform hover:scale-110 mt-1"
                >
                  <span class="text-2xl font-semibold leading-none mb-[7px]">+</span>
                </button>
                </div>
                <div class="flex justify-between items-center">
                  <div class="flex items-center space-x-2">
                    <div
                      v-for="user in editTaskData.assigned_users"
                      :key="user.user_id"
                      class="relative group"
                    >
                      <img
                        :src="getUserAvatar(user)"
                        :alt="user.firstName"
                        class="w-8 h-8 rounded-full border-2 border-white shadow hover:scale-110 transition"
                        :title="`${user.firstName} ${user.lastName}`"
                      />
                    </div>
                  </div>
                </div>
                <label class="font-semibold text-start text-lg text-gray-700 mt-3">Deadline</label>
              <input
                type="date"
                id="date"
                name="date"
                v-model="editTaskData.deadline"
                class="block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
              <div class="mt-5">
                <button
                  type="submit"
                  class="bg-blue-400 text-center text-lg font-semibold h-10 w-full rounded-lg shadow-md cursor-pointer translate-transform duration-300 transform hover:scale-105"
                >
                  Save
                </button>
             </div>
            </div>
              </div>
              
          <!-- MIDDLE DIVIDER -->
          <div class="border-l-2 border-gray-300 h-full"></div>

          <!-- RIGHT: Comments Section -->
          <div class="flex flex-col flex-1 p-6 bg-white h-full">
              <!-- Header -->
              <h2 class="text-xl font-semibold text-gray-700 mb-4 border-b pb-2">
                Comments
              </h2>

              <!-- Comment List -->
              <div
                class="flex-1 overflow-y-auto space-y-4 mb-4 p-2 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100"
              >
                <!-- Show if there are comments -->
               <template v-if="taskComments.length > 0">
                  <div
                    v-for="comment in taskComments"
                    :key="comment.comment_id"
                    class="p-3 bg-gray-100 rounded-lg shadow-sm"
                  >
                    <div class="flex items-center space-x-3">
                      <img
                        :src="getCommentAvatar(comment)"
                        class="w-9 h-9 rounded-full border"
                        :alt="comment.user_name"
                      />
                      <div>
                        <p class="font-medium text-gray-800 text-sm">
                          {{ comment.user_name }}
                        </p>
                        <p class="text-xs text-gray-400">
                          {{ formatDate(comment.created_at) }}
                        </p>
                      </div>
                    </div>

                    <!-- Message -->
                    <p class="text-gray-700 text-left text-sm mt-2 ml-12" v-if="comment.message">
                      {{ comment.message }}
                    </p>

                    <!-- Image (optional) -->
                    <div v-if="comment.image" class="mt-2 ml-12">
                      <img
                        :src="comment.image"
                        alt="Comment Image"
                        class="rounded-lg max-h-60 border cursor-pointer hover:opacity-90 transition"
                        @click="openImageModal(comment.image)"
                      />
                    </div>
                  </div>
                </template>
              </div>

              <!-- Add Comment (fixed bottom area inside box) -->
              <div class="bg-gray-100 rounded-lg px-3 py-2 shadow-inner mt-auto" @paste="handlePaste">
                
                <!-- Preview image (shown above input area) -->
                <div v-if="commentImagePreview" class="relative w-28 mb-3">
                  <img
                    :src="commentImagePreview"
                    alt="Comment Preview"
                    class="rounded-lg border object-cover w-28 h-28 shadow-md"
                  />
                  <button
                    type="button"
                    @click="removeCommentImage"
                    class="absolute top-1 right-1 bg-red-500 text-white rounded-full w-5 h-5 flex justify-center items-center hover:bg-red-600 transition cursor-pointer"
                    title="Remove Image"
                  >
                    &times;
                  </button>
                </div>

                <!-- File input (hidden) -->
                <input
                  type="file"
                  ref="commentImageInput"
                  accept="image/*"
                  class="hidden"
                  @change="handleCommentImage"
                />

                <!-- Input row -->
                <div class="flex items-center space-x-2">
                  <!-- Image upload icon -->
                  <button
                    type="button"
                    class="p-2 text-gray-500 hover:text-blue-500 transition cursor-pointer"
                    title="Attach Image"
                    @click="$refs.commentImageInput.click()"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="w-5 h-5"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-9-7h.01M5 7a2 2 0 012-2h10a2 2 0 012 2v10a2 2 0 01-2 2H7a2 2 0 01-2-2V7z"
                      />
                    </svg>
                  </button>

                  <!-- Comment input -->
                  <input
                    type="text"
                    v-model="newComment"
                    placeholder="Add a comment..."
                    class="flex-1 bg-transparent border-none outline-none text-gray-700 placeholder-gray-400"
                  />

                  <!-- Send button -->
                  <button
                    @click="addComment"
                    type="button"
                    class="p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition cursor-pointer"
                    title="Send Comment"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="w-5 h-5"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7" />
                    </svg>
                  </button>
                </div>
              </div>

          

            </div>
              
           </div>
         </div>
    </form>


  <!-- Edit Assign Modal -->
<div
  v-if="showEditAssignModal"
  @click.self="showEditAssignModal = false"
  class="fixed inset-0 bg-gray-800/40 flex justify-center items-center z-999"
>
  <div class="bg-white rounded-lg shadow-lg w-[450px] p-6 space-y-5">
    <h2 class="text-xl font-semibold text-gray-800">Reassign Task</h2>

    <div class="max-h-60 overflow-y-auto border rounded-lg p-3 space-y-2">
      <div
        v-for="user in users"
        :key="user.user_id"
        class="flex items-center space-x-2"
      >
        <input
          type="checkbox"
          :id="'edit-user-' + user.user_id"
          :value="user.user_id"
          v-model="editSelectedUserIds"
          class="cursor-pointer w-4 h-4 text-blue-600 border-gray-300 rounded"
        />
        <label :for="'edit-user-' + user.user_id" class="cursor-pointer text-gray-700">
          {{ user.firstName }} {{ user.lastName }}
        </label>
      </div>
    </div>

    <div class="flex justify-end space-x-3 mt-4">
      <button
        @click="showEditAssignModal = false"
        class="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 transition cursor-pointer"
      >
        Cancel
      </button>
      <button
        @click="confirmEditAssignUsers"
        class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition cursor-pointer"
      >
        Assign
      </button>
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
    <div
            v-if="showImageModal"
            class="fixed inset-0 bg-gray-800/50 flex justify-center items-center z-999"
            @click="closeImageModal"
          >
            <img :src="modalImageUrl" class="max-h-[90vh] rounded-lg shadow-lg" />
          </div>
  </div>
</template>

<script>
import axios from 'axios';
const COLORS = [
  'bg-blue-600',
  'bg-green-600',
  'bg-purple-600',
  'bg-pink-600',
  'bg-yellow-500',
  'bg-orange-500',
  'bg-red-600',
  'bg-teal-600',
  'bg-indigo-600',
  'bg-gray-500'
];

export default {
  name: 'Dashboard',
  data() {
    return {
      baseURL: 'http://127.0.0.1:5000',
      cardInfo: [],
      taskTypes: [],
      AddTaskTypeForm: false,
      colorMap: {},
      selectedTaskType: null,
      newTaskTypeName: '',
      showAlert: false,
      alertMessage: '',
      alertType: '',
      users: [],              
      selectedUserIds: [],    
      showAssignModal: false,
      title: '',   
      description: '',
      deadline: '',
      editTaskForm: false,
      editTaskData: {
          task_id: null,
          title: '',
          description: '',
          deadline: '',
          status: '',
          task_type_id: null,
          assigned_user_ids: []
        },
      editSelectedUserIds: [],
      showEditAssignModal: false,
      showStatusModal: false,
      statusOptions: ['Pending', 'In Progress', 'Done', 'Cancelled'],
      stats: {
        cancelled: { count:0, growth: 0 },
        ongoing: { count:0, growth: 0 },
        done: { count:0, growth: 0 }
      },
      taskComments: [],
      newComment: '',
      commentImage: null,
      commentImagePreview: null,
      showImageModal: false,
      modalImageUrl: null,
      
    };
  },
    mounted() {
      this.fetchTasks();
      this.fetchTaskTypes();
      this.fetchUsers();
      this.fetchStats();
      this.fetchComments();
    },


  methods: {

    openImageModal(url) {
      this.modalImageUrl = url;
      this.showImageModal = true;
    },

    closeImageModal() {
      this.showImageModal = false;
      this.modalImageUrl = null;
    },
    
   getColorClass(title) {
      if (this.colorMap[title]) return this.colorMap[title];
      const randomColor = COLORS[Math.floor(Math.random() * COLORS.length)];
      this.colorMap[title] = randomColor;
      return randomColor;
    },


    showAddTaskType() {
      this.AddTaskTypeForm = true;
    },

    closeAddTaskType()
    {
      this.AddTaskTypeForm = false;
    },

 async fetchTaskTypes() {
        try {
          const token = sessionStorage.getItem('access_token');
          if (!token) {
            console.error('No token found');
            this.$router.push('/'); 
            return;
          }

          const response = await axios.get(`${this.baseURL}/task_types`, {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          });

         
          this.taskTypes = response.data;

          console.log('Task types fetched:', this.taskTypes);
        } catch (error) {
          console.error('Error fetching task types:', error);
        }
      },


      selectTaskType(type) {
        if (this.editTaskForm) {
          // Editing mode
          this.editTaskData.task_type_id =
            this.editTaskData.task_type_id === type.task_type_id
              ? null
              : type.task_type_id;
        } else {
          // Creating new task
          this.selectedTaskType =
            this.selectedTaskType === type.task_type_id
              ? null
              : type.task_type_id;
        }
      },

    async addTaskType() {
          try {
            const token = sessionStorage.getItem('access_token');
            if (!token) {
              console.error('No token found');
              this.$router.push('/');
              return;
            }

            // Example: get task type name from an input field or modal
            const newTypeName = this.newTaskTypeName?.trim();
            if (!newTypeName) {
              this.showAlertMessage('No task type name provided');
              return;
            }

            const response = await axios.post(
              `${this.baseURL}/add_task_type`,
              { task_type_name: newTypeName },
              {
                headers: {
                  'Authorization': `Bearer ${token}`,
                  'Content-Type': 'application/json',
                },
              }
            );

            if (response.data.message) {
              this.showAlertMessage('success', response.data.message);
            }


            // Optional: refresh your task type list
            await this.fetchTaskTypes();

            // Clear input or close modal
            this.newTaskTypeName = '';
            this.AddTaskTypeForm = false;

          } catch (error) {
            console.error('Error adding task type:', error);
            this.showAlertMessage('error', 'Failed to add task type. Please try again.');
          }
        },

        showAlertMessage(type, message) {
          this.alertType = type;
          this.alertMessage = message;
          this.showAlert = true;
        },
        closeAlert() {
          this.showAlert = false;
          this.alertMessage = '';
          this.alertType = '';
        },

        async fetchUsers() {
          try {
            const token = sessionStorage.getItem('access_token');
            if (!token) return console.error('No token found');

            const response = await axios.get(`${this.baseURL}/users`, {
              headers: { 'Authorization': `Bearer ${token}` }
            });
            this.users = response.data;
          } catch (error) {
            console.error('Error fetching users:', error);
          }
        },

       openAssignModal() {
          this.showAssignModal = true;
          this.selectedUserIds = this.editTaskData.assigned_user_ids.map(u => u.user_id);
        },

        closeAssignModal() {
          this.showAssignModal = false;
        },

        confirmAssignUsers() {
          
          this.showAssignModal = false;
        },
        getUserName(userId) {
            const user = this.users.find((u) => u.user_id === userId);
            return user ? `${user.firstName} ${user.lastName}` : "Unknown";
          },

          getUserAvatar(user) {
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
          getCommentAvatar(comment) {
          return this.getUserAvatar({ image: comment.user_image });
        },

        handleCommentImage(event) {
          const file = event.target.files[0];
           if (file) {
            this.commentImage = file;

            // Preview
            const reader = new FileReader();
            reader.onload = (e) => {
              this.commentImagePreview = e.target.result;
            };
            reader.readAsDataURL(file);
        }
      },

      removeCommentImage() {
        this.commentImage = null;
        this.commentImagePreview = null;
      },

      handlePaste(event) {
        const items = (event.clipboardData || event.originalEvent.clipboardData).items;
        for (const item of items) {
          if (item.type.indexOf('image') !== -1) {
            const file = item.getAsFile();
            this.commentImage = file;

            // Preview
            const reader = new FileReader();
            reader.onload = (e) => {
              this.commentImagePreview = e.target.result;
            };
            reader.readAsDataURL(file);
          }
        }
      },


          async createTask() {
              // Prevent duplicate submissions
              if (this.isSubmitting) return;
              this.isSubmitting = true;

              try {
                const token = sessionStorage.getItem('access_token');
                if (!token) {
                  console.error('No token found');
                  this.$router.push('/');
                  return;
                }

                // Validate inputs
                if (!this.title || !this.description || !this.selectedTaskType || this.selectedUserIds.length === 0) {
                  this.showAlertMessage('error', 'Please fill in all required fields and assign at least one user.');
                  return;
                }

                const newTask = {
                  title: this.title.trim(),
                  description: this.description.trim(),
                  deadline: this.deadline,
                  task_type_id: this.selectedTaskType,
                  assigned_user_ids: this.selectedUserIds
                };

                const response = await axios.post(
                  `${this.baseURL}/create_task`,
                  newTask,
                  {
                    headers: {
                      'Authorization': `Bearer ${token}`,
                      'Content-Type': 'application/json',
                    },
                  }
                );

                if (response.status === 201 && response.data.message) {
                  this.showAlertMessage('success', response.data.message);

                  // Clear form
                  this.title = '';
                  this.description = '';
                  this.deadline = '';
                  this.selectedTaskType = null;
                  this.selectedUserIds = [];

                  // Refresh task list
                  await this.fetchTasks();
                } else {
                  this.showAlertMessage('error', 'Unexpected response from server.');
                }

              } catch (error) {
                console.error('Error creating task:', error);
                const message = error.response?.data?.error || 'Failed to create task. Please try again.';
                this.showAlertMessage('error', message);
              } finally {
                this.isSubmitting = false;
              }
            },

          async fetchTasks() {
              try {
                const token = sessionStorage.getItem('access_token');
                if (!token) {
                  console.error('No token found');
                  this.$router.push('/');
                  return;
                }

                const response = await axios.get(`${this.baseURL}/fetch_tasks`, {
                  headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json'
                  }
                });

                if (response.status === 200 && Array.isArray(response.data)) {
                  this.cardInfo = response.data;
                  console.log('Tasks fetched:', this.cardInfo);
                } else {
                  console.warn('Unexpected response format:', response);
                  this.cardInfo = [];
                }

              } catch (error) {
                console.error('Error fetching tasks:', error);
                this.cardInfo = [];
                this.showAlertMessage?.('error', 'Failed to load tasks. Please try again.');
              }
            },


    showEditTaskForm(task) {
      this.editTaskForm = true;
      this.editTaskData = {
        task_id: task.task_id,
        title: task.title,
        description: task.description,
        status: task.status,
        deadline: task.deadline ? new Date(task.deadline).toISOString().split('T')[0] : '',
        task_type_id: task.task_type?.task_type_id || null,
        assigned_users: task.users || [], 
        assigned_user_ids: task.users ? task.users.map(u => u.user_id) : [],
      };

      this.selectedTaskType = this.editTaskData.task_type_id;
      this.editSelectedUserIds = [...this.editTaskData.assigned_user_ids];

      // ✅ Fetch comments for this specific task
      this.fetchComments(task.task_id);
    },

    closeEditTaskForm() {
      this.editTaskForm = false;
      this.editTaskData = {};
      this.editSelectedUserIds = [];
    },

    openEditAssignModal() {
      this.showEditAssignModal = true;

      // If we have full user objects, extract their IDs
      if (this.editTaskData.assigned_users) {
        this.editSelectedUserIds = this.editTaskData.assigned_users.map(u => u.user_id);
      } else {
        this.editSelectedUserIds = [...this.editTaskData.assigned_user_ids];
      }
    },
    confirmEditAssignUsers() {
      // Update assigned IDs
      this.editTaskData.assigned_user_ids = [...this.editSelectedUserIds];

      // ✅ Also update the actual user objects
      this.editTaskData.assigned_users = this.users.filter(user =>
        this.editSelectedUserIds.includes(user.user_id)
      );

      // Close modal
      this.showEditAssignModal = false;
    },

    async updateTask() {
        try {
          const token = sessionStorage.getItem('access_token');
          if (!token) {
            console.error('No token found');
            this.$router.push('/');
            return;
          }

          // Validate fields
          if (!this.editTaskData.title || !this.editTaskData.description || !this.editTaskData.task_type_id) {
            this.showAlertMessage('error', 'Please fill in all required fields.');
            return;
          }

          const updatedTask = {
            title: this.editTaskData.title,
            description: this.editTaskData.description,
            deadline: this.editTaskData.deadline,
            task_type_id: this.editTaskData.task_type_id,
            assigned_user_ids: this.editTaskData.assigned_user_ids.map(u => 
            typeof u === "object" ? u.user_id : u
          )
          };

          const response = await axios.put(
            `${this.baseURL}/update_task/${this.editTaskData.task_id}`,
            updatedTask,
            {
              headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json',
              },
            }
          );

          if (response.data.message) {
            this.showAlertMessage('success', response.data.message);
          }

          await this.fetchTasks();

          this.editTaskForm = false;
          this.editTaskData = {
            task_id: null,
            title: '',
            description: '',
            deadline: '',
            task_type_id: null,
            assigned_user_ids: []
          };

        } catch (error) {
          console.error('Error updating task:', error);
          this.showAlertMessage('error', 'Failed to update task. Please try again.');
        }
      },
      formatDate(dateString, format = 'long') {
          if (!dateString) return '';

          const date = new Date(dateString);

          if (isNaN(date)) return dateString;

          const options =
            format === 'short'
              ? { year: 'numeric', month: 'short', day: 'numeric' } 
              : { year: 'numeric', month: 'long', day: 'numeric' }; 

          return date.toLocaleDateString('en-US', options);
        },

        openStatusModal() {
          this.selectedStatus = this.editTaskData.status;
          this.showStatusModal = true;
        },

        async updateStatus() {
          try {
            const response = await fetch(`http://localhost:5000/update_task_status/${this.editTaskData.task_id}`, {
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

          
            this.editTaskData.status = this.selectedStatus;
            this.showStatusModal = false;
            await this.fetchTasks(sessionStorage.getItem('user_id')); 
            await this.fetchStats();
            console.log(result.message);
          } catch (error) {
            console.error('Error updating status:', error);
            alert('Failed to update status.');
          }
        },

        pendingTasksCount() {
          return this.cardInfo.filter(task => task.status === 'Pending').length;
        },
        inProgressTasksCount() {
          return this.cardInfo.filter(task => task.status === 'In Progress').length;
        },
        doneTasksCount() {
          return this.cardInfo.filter(task => task.status === 'Done').length;
        },

        async fetchStats() {
          try {
            const res = await fetch('http://localhost:5000/task_stats');
            const data = await res.json();
            this.stats = data;
          } catch (error) {
            console.error('Failed to fetch stats:', error);
          }
        },

        async fetchComments(taskId) {
            try {
              const token = sessionStorage.getItem('access_token');
              if (!token) {
                console.error('No token found');
                this.$router.push('/');
                return;
              }

              const response = await axios.get(`${this.baseURL}/tasks/${taskId}/comments`, {
                headers: {
                  Authorization: `Bearer ${token}`,
                  'Content-Type': 'application/json'
                }
              });

              if (response.status === 200) {
                 if (Array.isArray(response.data) && response.data.length > 0) {
                  this.taskComments = [...response.data].reverse();
                  console.log(`Comments for task ${taskId}:`, this.taskComments);
                } else {
                  this.taskComments = [];
                  console.log(`No comments found for task ${taskId}.`);
                }
              } else {
                console.warn('Unexpected response format:', response);
                this.taskComments = [];
              }
            } catch (error) {
              // Only show snackbar for actual network or server errors
              if (error.response && error.response.status !== 404) {
                console.error('Error fetching comments:', error);
                this.showAlertMessage?.('error', 'Failed to load comments. Please try again.');
              } else {
                console.log(`No comments available for task ${taskId}.`);
              }
              this.taskComments = [];
            }
          },
          
     async addComment() {
        try {
          const token = sessionStorage.getItem('access_token');
          const userId = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');

          if (!token) {
            console.error('No token found');
            this.$router.push('/');
            return;
          }

          if (!this.newComment.trim() && !this.commentImage) {
            this.showAlertMessage('error', 'Comment cannot be empty.');
            return;
          }

          const formData = new FormData();
          formData.append('user_id', userId);
          formData.append('message', this.newComment.trim());
          if (this.commentImage) {
            formData.append('image', this.commentImage);
          }

          const response = await axios.post(
            `${this.baseURL}/tasks/${this.editTaskData.task_id}/comments`,
            formData,
            {
              headers: {
                Authorization: `Bearer ${token}`
               
              }
            }
          );

          if (response.status === 201) {
            this.showAlertMessage('success', 'Comment added successfully!');
            this.newComment = '';
            this.commentImage = null;
            this.commentImagePreview = null;
            await this.fetchComments(this.editTaskData.task_id);
          } else {
            this.showAlertMessage('error', 'Failed to add comment. Please try again.');
          }
        } catch (error) {
          console.error('Error adding comment:', error.response?.data || error);
          this.showAlertMessage('error', 'Failed to add comment. Please try again.');
        }
      },

      

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
