<template>
  <div class="h-[70px] bg-gray-100 flex items-center shadow-xl px-[20px] w-full py-[10px] z-10 shadow-md">
        <div class="w-full flex justify-between items-center">
          <h1 class="font-inter text-3xl font-bold">User Management</h1>
          <button class = "mr-2 w-32 h-9 bg-[#27A9F5] rounded-sm font-semibold text-gray-200
          transition-transform duration-300 transform hover:scale-105 cursor-pointer " @click="showInactivUsersModal">Inactive Users</button>
        </div>
  </div>

<div class="p-6 overflow-y-auto">
  
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

    <!-- Status Confirmation Modal -->
        <div v-if="showStatusConfirmModal" @click.self="closeStatusConfirmModal" class="fixed inset-0 bg-gray-800/20 overflow-y-auto flex justify-center items-center z-100">
          <div class="bg-white p-5 rounded-lg shadow-lg w-[400px]">
            <div class="flex flex-col items-center">
              <h2 class="text-xl font-semibold mb-4">Confirm Status Change</h2>
              <p class="mb-6 text-center">Are you sure you want to change the user status?</p>
              <div class="flex space-x-4">             
                <button 
                  @click="closeStatusConfirmModal" 
                  class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-opacity-90 cursor-pointer transfomr-transition duration-300 transform hover:scale-105">
                  Cancel
                </button>
                <button 
                  @click="confirmStatusChange" 
                  class = "w-20 h-10 bg-blue-500 text-gray-100 font-semibold rounded-lg shadow-md cursor-pointer transform-transition duration-300 transform hover:scale-105">
                  Yes
                </button>
              </div>
            </div>
          </div>
        </div>



        <!-- Inactive Users Modal -->
        <div v-if="showInactiveUsersModal" @click.self="closeInactiveUsersModal" class="fixed inset-0 bg-gray-800/20 overflow-y-auto flex justify-center items-center z-50">
          <div class="bg-white p-5 rounded-lg shadow-lg w-[1000px]">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-xl font-semibold">Inactive Users</h2>
              <button @click="closeInactiveUsersModal" class="text-gray-500 hover:text-gray-700 cursor-pointer">
                <span class="text-2xl">&times;</span>
              </button>
            </div>

            <div class="overflow-x-auto">
              <table class="w-full text-sm text-left text-gray-500">
                <thead class="text-xs text-gray-700 uppercase bg-gray-50">
                  <tr>
                    <th scope="col" class="w-16 px-2 py-3">#</th>
                    <th scope="col" class="w-52 px-2 py-3">Name</th>
                    <th scope="col" class="w-52 px-2 py-3">Email</th>
                    <th scope="col" class="w-40 px-2 py-3">Contact</th>
                    <th scope="col" class="w-36 px-2 py-3">Address</th>
                    <th scope="col" class="w-28 px-2 py-3">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(user, index) in inactiveUsers" :key="user.user_id" 
                      class="bg-white border-b hover:bg-gray-50">
                    <td class="px-6 py-4">{{ index + 1 }}</td>
                    <td class="w-52 px-2 py-3 truncate">{{ user.firstName }} {{ user.lastName }}</td>
                    <td class="w-52 px-2 py-3 truncate">{{ user.email }}</td>
                    <td class="w-40 px-2 py-3 truncate">{{ user.contact }}</td>
                    <td class="w-36 px-2 py-3 truncate">{{ user.address}}</td>
                    <td class="px-6 py-4">
                      <button
                        class="p-2 hover:opacity-80 transform hover:scale-110 transition-transform duration-200 cursor-pointer"
                        @click="toggleUserStatus(user)"
                        title="Set User to Active">
                        <img src="../assets/icons/activate.png" alt="Set Active" class="w-5 h-5">
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

  <div class="flex flex-row items-center m-5 space-x-5">
        <div class="flex justify-start w-52 h-20 bg-white rounded-lg shadow-lg px-2 items-center border-l-2 border-blue-400 space-x-5">
            <h2 class="font-inter text-4xl font-bold mb-0"> {{ staffs.length }} <span class = "text-sm antialiased text-gray-600">staff</span></h2>
        </div>
        <div class="flex justify-start w-52 h-20 bg-white rounded-lg shadow-lg px-2 items-center border-l-2 border-blue-400 space-x-5">
            <h2 class="font-inter text-4xl font-bold mb-0"> {{ admins.length }} <span class = "text-sm antialiased text-gray-600">admin</span></h2>
        </div>
        <div class="flex justify-start w-52 h-20 bg-white rounded-lg shadow-lg px-2 items-center border-l-2 border-blue-400 space-x-5">
            <h2 class="font-inter text-4xl font-bold mb-0"> {{ clients.length }} <span class = "text-sm antialiased text-gray-600">client</span></h2>
        </div>
        <form class="flex items-center w-[300px] mt-9">
              <label for="voice-search" class="sr-only">Search</label>
              <div class="relative w-full">
                <div class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none">
                  <svg aria-hidden="true" class="w-5 h-auto text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"></path>
                  </svg>
                </div>
                <input type="text" id="search-bar" class="bg-gray-50 border font-inter border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search Account..." required v-model="searchAccount">
                <router-link to="/" class="flex absolute inset-y-0 right-0 items-center pr-3">
                  <svg aria-hidden="true" class="w-4 h-4 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  </svg>
                </router-link>
              </div>
        </form>
      </div>

      <div class="flex flex-row justify-between items-center m-5 space-x-5">
        <div class = "flex">
        <button :class="[ 
          'flex justify-center items-center w-28 h-10 m-2 font-inter font-semibold rounded-lg shadow-lg transition-transform duration-300 transform hover:scale-105 cursor-pointer', 
          { 'bg-gray-800 text-white': showTable === 'Staffs', 'bg-white': showTable !== 'Staffs' } 
        ]" @click="showTable = 'Staffs'">
          Staff
        </button>
        <button :class="[ 
          'flex justify-center items-center w-28 h-10 m-2 font-inter font-semibold rounded-lg shadow-lg transition-transform duration-300 transform hover:scale-105 cursor-pointer', 
          { 'bg-gray-800 text-white': showTable === 'Admin', 'bg-white': showTable !== 'Admin' } 
        ]" @click="showTable = 'Admin'">
          Admin
        </button>
        <button :class="[ 
          'flex justify-center items-center w-28 h-10 m-2 font-inter font-semibold rounded-lg shadow-lg transition-transform duration-300 transform hover:scale-105 cursor-pointer', 
          { 'bg-gray-800 text-white': showTable === 'Client', 'bg-white': showTable !== 'Client' } 
        ]" @click="showTable = 'Client'">
          Client
        </button>
      </div>
      <button class = "mr-2 w-32 h-10 bg-[#27A9F5] font-semibold text-gray-100 font-inter rounded-md shadow-lg 
      transition-transform duration-300 transform hover:scale-105 cursor-pointer" @click="addUserBtn">
        Add Account
      </button>
     </div>

<!--- Staff Table--->
  <div v-if="showTable === 'Staffs'" class="relative shadow-md sm:rounded-xl w-full max-w-[1600px] h-[200] ml-5 mt-2 font-inter mb-10">
    <div class="overflow-x-auto">
      <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400 mb-4 max-h-30 table-fixed">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th scope="col" class="w-16 px-2 py-3">#</th>
          <th scope="col" class="w-52 px-2 py-3">Name</th>
          <th scope="col" class="w-52 px-2 py-3">Email</th>
          <th scope="col" class="w-40 px-2 py-3">Contact</th>
          <th scope="col" class="w-36 px-2 py-3">Address</th>
          <th scope="col" class="w-28 px-2 py-3">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr
            v-for="(staff, index) in paginatedStaffs"
            :key="staff.no"
            class="border-b dark:border-gray-700 odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800">
          <th scope="row" class="w-16 px-2 py-3 font-inter text-gray-900 whitespace-nowrap dark:text-white">{{ staff.dummyIndex }}</th>
          <td class="w-52 px-2 py-3 truncate">{{ staff.firstName }} {{ staff.lastName }}</td>
          <td class="w-52 px-2 py-3 truncate">{{ staff.email }}</td>
          <td class="w-40 px-2 py-3 truncate">{{ staff.contact }}</td>
          <td class="w-36 px-2 py-3 truncate">{{ staff.address}}</td>

          <td class="w-28 px-2 py-3">
            <button class="p-2 hover:opacity-80 transform hover:scale-110 transition-transform duration-200 cursor-pointer" 
            @click="openUpdateUserForm(index)" 
            title="Update Staff Info">
            <img src="../assets/icons/edit.png" alt="Update" class="w-5 h-5">
           
              </button>
            <button class="p-2 hover:opacity-80 transform hover:scale-110 transition-transform duration-200 cursor-pointer" 
            @click="openStatusConfirmModal(staff)" 
            title="Set User to Inactive">
            <img src="../assets/icons/deactivate.png" alt="Update" class="w-5 h-5">
           
              </button>
          </td>
        </tr>
      </tbody>
    </table>

      <!-- Pagination Controls -->
      <div class="flex justify-center space-x-2 mt-4 mb-6">
        <button @click="prevStaffsPage" :disabled="currentStaffsPage === 1" 
            class="px-3 py-1 bg-[#27A9F5] text-white rounded-md hover:bg-[#0297F0] disabled:opacity-50 text-sm cursor-pointer">Previous</button>
        <button v-for="page in totalStaffsPages" :key="page" @click="changeStaffsPage(page)" 
            :class="{'bg-[#27A9F5]': currentStaffsPage === page, 'bg-gray-300': currentStaffsPage !== page}" 
            class="px-3 py-1 text-white rounded-md hover:bg-[#0297F0] text-xs cursor-pointer">
          {{ page }}
        </button>
        <button @click="nextStaffsPage" :disabled="currentStaffsPage === totalStaffsPages" 
            class="px-3 py-1 bg-[#27A9F5] text-white rounded-md hover:bg-[#0297F0] disabled:opacity-50 text-xs cursor-pointer">Next</button>
      </div>
    </div>
  </div>

  <!--- Admin Table--->
  <div v-if="showTable === 'Admin'" class="relative shadow-md sm:rounded-xl w-full max-w-[1600px] h-[200] ml-5 mt-2 font-inter mb-10">
    <div class="overflow-x-auto">
      <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400 mb-4 max-h-30 table-fixed">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th scope="col" class="w-16 px-2 py-3">#</th>
          <th scope="col" class="w-52 px-2 py-3">Name</th>
          <th scope="col" class="w-52 px-2 py-3">Email</th>
          <th scope="col" class="w-40 px-2 py-3">Contact</th>
          <th scope="col" class="w-36 px-2 py-3">Address</th>
          <th scope="col" class="w-28 px-2 py-3">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr
            v-for="(admin, index) in paginatedAdmin"
            :key="admin.no"
            class="border-b dark:border-gray-700 odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800">
          <th scope="row" class="w-16 px-2 py-3 font-inter text-gray-900 whitespace-nowrap dark:text-white">{{ admin.dummyIndex }}</th>
          <td class="w-52 px-2 py-3 truncate">{{ admin.firstName }} {{ admin.lastName }}</td>
          <td class="w-52 px-2 py-3 truncate">{{ admin.email }}</td>
          <td class="w-40 px-2 py-3 truncate">{{ admin.contact }}</td>
          <td class="w-36 px-2 py-3 truncate">{{ admin.address }}</td>

          <td class="w-28 px-2 py-3">
            <button class="p-2 hover:opacity-80 transform hover:scale-110 transition-transform duration-200 cursor-pointer" 
            @click="openUpdateUserForm(index)" 
            title="Update Admin Info">
            <img src="../assets/icons/edit.png" alt="Update" class="w-5 h-5">
           
              </button>
            <button class="p-2 hover:opacity-80 transform hover:scale-110 transition-transform duration-200 cursor-pointer" 
            @click="openStatusConfirmModal(admin)" 
            title="Set User to Inactive">
            <img src="../assets/icons/deactivate.png" alt="Update" class="w-5 h-5">
           
              </button>
          </td>
        </tr>
      </tbody>
    </table>

      <!-- Pagination Controls -->
      <div class="flex justify-center space-x-2 mt-4 mb-6">
        <button @click="prevStaffsPage" :disabled="currentStaffsPage === 1" 
            class="px-3 py-1 bg-[#27A9F5] text-white rounded-md hover:bg-[#0297F0] disabled:opacity-50 text-sm cursor-pointer">Previous</button>
        <button v-for="page in totalAdminPages" :key="page" @click="changeAdminPage(page)" 
            :class="{'bg-[#27A9F5]': currentAdminPage === page, 'bg-gray-300': currentAdminPage !== page}" 
            class="px-3 py-1 text-white rounded-md hover:bg-[#0297F0] text-xs cursor-pointer">
          {{ page }}
        </button>
        <button @click="nextAdminPage" :disabled="currentStaffsPage === totalAdminPages" 
            class="px-3 py-1 bg-[#27A9F5] text-white rounded-md hover:bg-[#0297F0] disabled:opacity-50 text-xs cursor-pointer">Next</button>
      </div>
    </div>
  </div>

    <!--Client Table-->
  <div v-if="showTable === 'Client'" class="relative shadow-md sm:rounded-xl w-full max-w-[1600px] h-[200] ml-5 mt-2 font-inter mb-10">
    <div class="overflow-x-auto">
      <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400 mb-4 max-h-30 table-fixed">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th scope="col" class="w-16 px-2 py-3">#</th>
          <th scope="col" class="w-52 px-2 py-3">Name</th>
          <th scope="col" class="w-52 px-2 py-3">Email</th>
          <th scope="col" class="w-40 px-2 py-3">Contact</th>
          <th scope="col" class="w-36 px-2 py-3">Address</th>
          <th scope="col" class="w-28 px-2 py-3">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr
            v-for="(client, index) in paginatedClients"
            :key="client.no"
            class="border-b dark:border-gray-700 odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800">
          <th scope="row" class="w-16 px-2 py-3 font-inter text-gray-900 whitespace-nowrap dark:text-white">{{ client.dummyIndex }}</th>
          <td class="w-52 px-2 py-3 truncate">{{ client.firstName }} {{ client.lastName }}</td>
          <td class="w-52 px-2 py-3 truncate">{{ client.email }}</td>
          <td class="w-40 px-2 py-3 truncate">{{ client.contact }}</td>
          <td class="w-36 px-2 py-3 truncate">{{ client.address }}</td>

          <td class="w-28 px-2 py-3">
            <button class="p-2 hover:opacity-80 transform hover:scale-110 transition-transform duration-200 cursor-pointer" 
            @click="openUpdateUserForm(index)" 
            title="Update Client Info">
            <img src="../assets/icons/edit.png" alt="Update" class="w-5 h-5">
           
              </button>
            <button class="p-2 hover:opacity-80 transform hover:scale-110 transition-transform duration-200 cursor-pointer" 
            @click="openStatusConfirmModal(client)" 
            title="Set User to Inactive">
            <img src="../assets/icons/deactivate.png" alt="Update" class="w-5 h-5">
           
              </button>
          </td>
        </tr>
      </tbody>
    </table>

      <!-- Pagination Controls -->
      <div class="flex justify-center space-x-2 mt-4 mb-6">
        <button @click="prevClientPage" :disabled="currentClientPage === 1" 
            class="px-3 py-1 bg-[#27A9F5] text-white rounded-md hover:bg-[#0297F0] disabled:opacity-50 text-sm cursor-pointer">Previous</button>
        <button v-for="page in totalClientPages" :key="page" @click="changeClientPage(page)" 
            :class="{'bg-[#27A9F5]': currentClientPage === page, 'bg-gray-300': currentClientPage !== page}" 
            class="px-3 py-1 text-white rounded-md hover:bg-[#0297F0] text-xs cursor-pointer">
          {{ page }}
        </button>
        <button @click="nextClientPage" :disabled="currentClientPage === totalClientPages" 
            class="px-3 py-1 bg-[#27A9F5] text-white rounded-md hover:bg-[#0297F0] disabled:opacity-50 text-xs cursor-pointer">Next</button>
      </div>
    </div>
  </div>

   <!-- Add User Form -->
 <form v-if="addUserForm" @submit.prevent="handleRegister" class="fixed inset-0 bg-gray-800/40 z-40 overflow-y-auto flex justify-center items-center" @click.self="closeAddUserForm">
  <div class="bg-white w-[550px] p-5 rounded-lg shadow-lg overflow-y-auto">
    <div class="flex justify-between items-center m-3">
      <h1 class="font-semibold text-xl font-inter text-gray-800">Add Account</h1>
    </div>
    <div class="border border-gray-500 mt-5 items-center"></div>
    <div class="m-5">
      <span class = "text-red-500"> {{ errorMessage }}</span>
      <!-- First Name and Last Name -->
      <div class="flex flex-row">
        <div class="flex flex-col space-y-1 w-full">
          <input type="text" class="p-2 h-12 rounded-lg text-sm shadow-sm border border-gray-500/20 focus:outline-none focus:border-blue-700"
           v-model="firstname" placeholder ="First Name" required>
        </div>
        <div class="flex flex-col space-y-1 w-full ml-2">
          <input type="text" class="p-2 h-12 rounded-lg text-sm shadow-sm border border-gray-500/20 focus:outline-none focus:border-blue-700"
           v-model="lastname" placeholder ="Last Name"  required>
        </div>
      </div>

      <!-- Username -->
      <div class="flex flex-col mt-5">
        <input type="text" class="mt-1 p-2 w-full h-12 rounded-lg text-sm shadow-sm border border-gray-500/20 focus:outline-none focus:border-blue-700"
         v-model="username" placeholder="Username" @click="deriveUsername" required>
      </div>

      <!-- Email -->
      <div class="flex flex-col  mt-5">
        <input type="text" class="mt-1 p-2 w-full h-12 rounded-lg text-sm shadow-sm border border-gray-500/20 focus:outline-none focus:border-blue-700" v-model="email"
         @click="deriveEmail" placeholder="Email" required>
      </div>

      <!-- Contact Number -->
      <div class="flex flex-col  mt-5">
        <input type="text" class="mt-1 p-2 w-full h-12 rounded-lg text-sm shadow-sm border border-gray-500/20 focus:outline-none focus:border-blue-700"
         v-model="contact" placeholder="Contact Number" maxlength="11" required>
      </div>

      <!-- Address -->
      <div class="flex flex-col  mt-5">
        <input type="text" class="mt-1 p-2 w-full h-12 rounded-lg text-sm shadow-sm border border-gray-500/20 focus:outline-none focus:border-blue-700"
         v-model="address" placeholder="Adress" required>
      </div>

      <!-- User Type Selection -->
      <div class="flex flex-col mt-5">
        <select class="flex mt-1 p-2 w-full h-12 rounded-lg text-sm shadow-md border border-gray-500/20 focus:outline-none focus:border-blue-700" v-model="selectedUserType" @change="selectAddForm">
          <option value="" disabled class="text-gray-500">Select Account Type</option>
          <option value="staff">Staff</option>
          <option value="admin">Admin</option>
          <option value="client">Client</option>
          
        </select>
      </div>
      <!-- Confirm Button -->
      <div class="flex justify-end items-center mt-5 space-x-2">
          <button class="bg-gray-300 text-white w-20 h-10 rounded-lg transform-transition duration-300 transform hover:scale-105 hover:bg-gray-400 cursor-pointer" @click="closeAddUserForm">
          Cancel
        </button>
        <button type="submit" class="w-20 h-10 bg-blue-500 text-gray-100 font-semibold rounded-lg shadow-md transform-transition duration-300 transform hover:scale-105 cursor-pointer">
          Save
        </button>
      </div>
    </div>
  </div>
</form>


<!-- Update User Form -->
 <form v-if="updateUserForm" @submit.prevent="updateUserAccount" class="fixed inset-0 bg-gray-800/40 z-40 overflow-y-auto flex justify-center items-center" @click.self="closeUpdateUserForm">
  <div class="bg-white w-[550px] p-5 rounded-lg shadow-lg overflow-y-auto">
    <div class="flex justify-between items-center m-3">
      <h1 class="font-semibold text-xl font-inter text-gray-800">Update Account</h1>
    </div>
    <div class="border border-gray-500 mt-5 items-center"></div>
    <div class="m-5">
      <span class = "text-red-500"> {{ errorMessage }}</span>
      <!-- First Name and Last Name -->
      <div class="flex flex-row">
        <div class="flex flex-col space-y-1 w-full">
          <input type="text" class="p-2 h-12 rounded-lg text-sm shadow-sm border border-gray-500/20 focus:outline-none focus:border-blue-700"
           v-model="selectedUser.firstname" placeholder ="First Name">
        </div>
        <div class="flex flex-col space-y-1 w-full ml-2">
          <input type="text" class="p-2 h-12 rounded-lg text-sm shadow-sm border border-gray-500/20 focus:outline-none focus:border-blue-700"
           v-model="selectedUser.lastname" placeholder ="Last Name">
        </div>
      </div>

      <!-- Username -->
      <div class="flex flex-col mt-5">
        <input type="text" class="mt-1 p-2 w-full h-12 rounded-lg text-sm shadow-sm border border-gray-500/20 focus:outline-none focus:border-blue-700"
         v-model="selectedUser.username" placeholder="Username" @click="deriveUsername">
      </div>

      <!-- Email -->
      <div class="flex flex-col  mt-5">
        <input type="text" class="mt-1 p-2 w-full h-12 rounded-lg text-sm shadow-sm border border-gray-500/20 focus:outline-none focus:border-blue-700" v-model="selectedUser.email"
         @click="deriveEmail" placeholder="Email">
      </div>

      <!-- Contact Number -->
      <div class="flex flex-col  mt-5">
        <input type="text" class="mt-1 p-2 w-full h-12 rounded-lg text-sm shadow-sm border border-gray-500/20 focus:outline-none focus:border-blue-700"
         v-model="selectedUser.contact" placeholder="Contact Number" maxlenght="11">
      </div>

      <!-- Address -->
      <div class="flex flex-col  mt-5">
        <input type="text" class="mt-1 p-2 w-full h-12 rounded-lg text-sm shadow-sm border border-gray-500/20 focus:outline-none focus:border-blue-700"
         v-model="selectedUser.address" placeholder="Adress">
      </div>

      <!-- User Type Selection -->
      <div class="flex flex-col mt-5">
        <select class="flex mt-1 p-2 w-full h-12 rounded-lg text-sm shadow-md border border-gray-500/20 focus:outline-none focus:border-blue-700" v-model="selectedUser.user_type" @change="selectAddForm">
          <option value="" disabled class="text-gray-500">Select Account Type</option>
          <option value="staff">Staff</option>
          <option value="admin">Admin</option>
          <option value="client">Client</option>
        </select>
      </div>
      <!-- Confirm Button -->
      <div class="flex justify-end items-center mt-5 space-x-2">
          <button class="bg-gray-300 text-white w-20 h-10 rounded-lg transform-transition duration-300 transform hover:scale-105 hover:bg-gray-400 cursor-pointer" @click="closeUpdateUserForm">
          Cancel
        </button>
        <button type="submit" class="w-20 h-10 bg-blue-500 text-gray-100 font-semibold rounded-lg shadow-md transform-transition duration-300 transform hover:scale-105 cursor-pointer">
          Save
        </button>
      </div>
    </div>
  </div>
</form>
      
</div>

</template>

<script>
import axios from 'axios'


export default {
  name: 'ManageUsers',
  
  data() {
    return {
      baseURL: 'http://127.0.0.1:5000',
      showTable: 'Staffs',
      currentStaffsPage: 1,
      staffsPerPage: 5,
      searchAccount: '',
      currentAdminPage: 1,
      adminsPerPage: 5,
      currentClientPage: 1,
      clientsPerPage: 5,

      addUserForm: false,
      pendingUser: null,
      showStatusConfirmModal: false,

      firstname: '',
      lastname: '',
      username: '',
      email: '',
      contact: '',
      address: '',
      errorMessage: '',
      selectedUserType: '',
      status: '',

      showAlert: false,
      alertType: 'success',
      alertMessage: '',

      staffs: [],
      admins: [],
      clients: [],
      inactiveUsers: [],

      updateUserForm: false,
      selectedUser: {
        firstname: '',
        lastname: '',
        email: '',
        username: '',
        contact: '',
        address: '',
        user_type: '',
        status: ''
      },

      showInactiveUsersModal: false,

      



    };
  },
  computed: {
        filteredStaffs() {
          return this.staffs.filter(staff => 
            staff.fullName?.toLowerCase().includes(this.searchAccount.toLowerCase()) ||
            staff.email?.toLowerCase().includes(this.searchAccount.toLowerCase())
          );
        },
        
        filteredAdmins() {
          return this.admins.filter(admin => 
            admin.fullName?.toLowerCase().includes(this.searchAccount.toLowerCase()) ||
            admin.email?.toLowerCase().includes(this.searchAccount.toLowerCase())
          );
        },

        totalStaffsPages() {
          
          return Math.ceil(this.filteredStaffs.length / this.staffsPerPage);
        },

        totalAdminPages() {
          return Math.ceil(this.filteredAdmins.length / this.adminsPerPage);
        },

        paginatedStaffs() {
          const start = (this.currentStaffsPage - 1) * this.staffsPerPage;
          const end = start + this.staffsPerPage;
          return this.filteredStaffs.map((staff, index) => ({
            ...staff,
            dummyIndex: start + index + 1
          })).slice(start, end);
        },

        paginatedAdmin() {
          const start = (this.currentAdminPage - 1) * this.adminsPerPage;
          const end = start + this.adminsPerPage;
          return this.filteredAdmins.map((admin, index) => ({
            ...admin,
            dummyIndex: start + index + 1
          })).slice(start, end);
        },


        filteredClients() {
          return this.clients.filter(client => 
              client.fullName?.toLowerCase().includes(this.searchAccount.toLowerCase()) ||
              client.email?.toLowerCase().includes(this.searchAccount.toLowerCase())
          );
      },

    totalClientPages() {
        return Math.ceil(this.filteredClients.length / this.clientsPerPage);
    },

     paginatedClients() {   
          if (!Array.isArray(this.filteredClients)) {
              return []; 
          }

          const start = (this.currentClientPage - 1) * this.clientsPerPage;
          const end = start + this.clientsPerPage;

          return this.filteredClients
              .slice(start, end)
              .map((client, index) => ({
                  ...client,
                  dummyIndex: start + index + 1
              }));
      },
      },
  methods: {
   
    prevStaffsPage() {
      if (this.currentStaffsPage > 1) {
        this.currentStaffsPage--;
      }
    },
    nextStaffsPage() {
      if (this.currentStaffsPage < this.totalStaffsPages) {
        this.currentStaffsPage++;
      }
    },
    changeStaffsPage(page) {
      this.currentStaffsPage = page;
    },
    prevAdminPage() {
      if (this.currentAdminPage > 1) {
        this.currentAdminPage--;
      }
    },
    nextAdminPage() {
      if (this.currentAdminPage < this.totalAdminPages) {
        this.currentAdminPage++;
      }
    },
    changeAdminPage(page) {
      this.currentAdminPage = page;
    },
    prevClientPage() {
        if (this.currentClientPage > 1) {
            this.currentClientPage--;
        }
    },
    nextClientPage() {
        if (this.currentClientPage < this.totalClientPages) {
            this.currentClientPage++;
        }
    },
    changeClientPage(page) {
        this.currentClientPage = page;
    },


    addUserBtn() {
      this.addUserForm = true;
    },
    closeAddUserForm() {
      this.addUserForm = false;
    },

    async handleRegister() {
            try {
                const userType = localStorage.getItem('user_type') || sessionStorage.getItem('user_type');
                if (userType !== 'admin') {
                    this.showErrorAlert('Only admins can add new users.');
                    this.resetRegisterForm();
                    this.closeAddUserForm();
                    return;
                }
                
                const fields = [
                    this.username, this.email, this.firstname, this.lastname,
                    this.contact, this.address,
                ];

                if (fields.some(field => !field)) {
                    this.showErrorAlert('All fields are required!');
                    return;
                }

                
                if (this.username) {
                    this.registerPassword = this.username;
                }
               
                const requestData = {
                    email: this.email,
                    username: this.username,
                    firstname: this.firstname,
                    lastname: this.lastname,
                    contact: this.contact,
                    address: this.address,
                    password: this.registerPassword,
                    user_type: this.selectedUserType,
                    status: 'Active' 
                };

                
                const response = await axios.post(`${this.baseURL}/addAccount`, requestData);

                if (response.status === 201) {
                    this.showSuccessAlert('User added successfully!');
                    await this.fetchUsers();
                    this.resetRegisterForm(); 
                    this.closeAddUserForm();
                }
            } catch (error) {
                
                if (error.response?.data?.message) {
                    this.showErrorAlert(error.response.data.message);
                } else {
                    this.showErrorAlert('An error occurred. Please try again.');
                }
            }
        },

        resetRegisterForm() {
            this.email = '';
            this.username = '';
            this.firstname = '';
            this.lastname = '';
            this.contact = '';
            this.address = '';
            this.registerPassword = '';
            this.selectedUserType = '';
            this.service = '';
            this.errorMessage = '';
        },


    async fetchUsers() {
        try {
            const token = sessionStorage.getItem('access_token');
            if (!token) {
                console.error('No token found');
                this.$router.push('/'); 
                return;
            }

            const response = await axios.get(`${this.baseURL}/users`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.data) {
                console.log('API Response:', response.data);
                
                // Get the current logged-in user's ID or email
                const loggedInUserId = sessionStorage.getItem('user_id'); 
                const loggedInUserEmail = sessionStorage.getItem('email'); 

                // Filter users by status = 'Active'
                const activeUsers = response.data.filter(user => user.status === 'Active');

                // Exclude the logged-in user from the list
                const filteredActiveUsers = activeUsers.filter(user => 
                    user.user_id !== loggedInUserId && user.email !== loggedInUserEmail
                );

                // Separate admins and staff based on user_type
                this.admins = filteredActiveUsers.filter(user => user.user_type.toLowerCase() === 'admin');
                this.staffs = filteredActiveUsers.filter(user => user.user_type.toLowerCase() === 'staff');
                this.clients = filteredActiveUsers.filter(user => user.user_type.toLowerCase() === 'client');
                
                console.log('Filtered Active Admins:', this.admins);
                console.log('Filtered Active Staff:', this.staffs);
                console.log('Filtered Active Staff:', this.client);
            }
        } catch (error) {
            console.error('Error fetching users:', error);
            if (error.response?.status === 401) {
                localStorage.removeItem('access_token');
                sessionStorage.removeItem('acess_token');
                this.$router.push('/'); 
                console.error('Error response:', error.response.data);
            }
        }
    },

    getAuthToken() {
      return localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
  },



    showSuccessAlert(message) {
      this.alertType = 'success';
      this.alertMessage = message;
      this.showAlert = true;
    },
    showErrorAlert(message) {
      this.alertType = 'error';
      this.alertMessage = message;
      this.showAlert = true;
    },
    closeAlert() {
      this.showAlert = false;
      this.alertMessage = '';
    },

   openUpdateUserForm(index) {
          let user;

          if (this.showTable === 'Staffs') {
            user = this.staffs?.[index];
          } else if (this.showTable === 'Admin') {
            user = this.admins?.[index];
          } else if (this.showTable === 'Client') {
            user = this.clients?.[index];
          }

          if (!user) {
            console.warn('User not found for index:', index);
            return;
          }

          this.selectedUser = {
            user_id: user.user_id,
            firstname: user.firstname || user.firstName,
            lastname: user.lastname || user.lastName,
            email: user.email,
            username: user.username,
            contact: user.contact,
            address: user.address,
            user_type: user.user_type
          };

          this.updateUserForm = true;
        },

  closeUpdateUserForm() {
    this.updateUserForm = false;
  },

    async updateUserAccount() {
      try {

        const userType = localStorage.getItem('user_type') || sessionStorage.getItem('user_type');
                if (userType !== 'admin') {
                    this.showErrorAlert('Only admins can update users.');
                    this.closeUpdateUserForm();
                    return;
         }


        const token = localStorage.getItem('access_token');
        if (!token) {
          console.error('No token found');
          this.showErrorAlert('Authentication token missing. Please log in again.');
          return;
        }

        // Ensure user_id is included in the payload
        if (!this.selectedUser?.user_id) {
          console.error('User ID missing in selectedUser');
          this.showErrorAlert('User ID is required to update account.');
          return;
        }

        const response = await axios.put(`${this.baseURL}/update_account/${this.selectedUser.user_id}`, this.selectedUser, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.status === 200) {
          this.showSuccessAlert('User updated successfully!');
          this.closeUpdateUserForm();
          this.fetchUsers(); 
        }
      } catch (error) {
        console.error('Error updating user:', error);

        if (error.response?.data?.error) {
          this.showErrorAlert(error.response.data.error);
        } else if (error.message === 'Network Error') {
          this.showErrorAlert('Network error. Please check your connection or CORS settings.');
        } else {
          this.showErrorAlert('An error occurred. Please try again.');
        }
      }
    },

    openStatusConfirmModal(user) {
        this.pendingUser = user;
        this.showStatusConfirmModal = true;
      },

      toggleUserStatus(user) {
          this.pendingUser = user;
          this.showStatusConfirmModal = true;
        },

     async confirmStatusChange() {
          try {
            const userType = localStorage.getItem('user_type') || sessionStorage.getItem('user_type');
                if (userType !== 'admin') {
                    this.showErrorAlert('Only admins can change user status.');
                    return;
            }


            if (!this.pendingUser) {
              console.error('No user selected for status change');
              return;
            }

            const token = localStorage.getItem('access_token');
            if (!token) {
              console.error('No token found');
              return;
            }

            const newStatus = this.pendingUser.status === 'Active' ? 'Inactive' : 'Active';

            const response = await axios.put(
              `${this.baseURL}/update_status/${this.pendingUser.user_id}`,
              { status: newStatus },
              {
                headers: {
                  'Authorization': `Bearer ${token}`,
                  'Content-Type': 'application/json'
                }
              }
            );

            if (response.status === 200) {
              this.showSuccessAlert(`User status changed to ${newStatus}`);
              await this.fetchUsers(); 
              await this.fetchInactiveUsers(); 
              this.closeStatusConfirmModal();
            }
          } catch (error) {
            console.error('Error toggling user status:', error);
            this.showErrorAlert(error.response?.data?.message || 'Error updating user status');
            this.closeStatusConfirmModal();
          }
        },

      closeStatusConfirmModal() {
        this.showStatusConfirmModal = false;
      },


      async fetchInactiveUsers() {
        try {
          const token = localStorage.getItem('access_token');
          if (!token) {
            console.error('No token found');
            return;
          }

          const response = await axios.get('http://127.0.0.1:5000/inactive_users', {
            headers: {
              Authorization: `Bearer ${token}`, 
            },
          });

          if (response.status === 200) {
            this.inactiveUsers = response.data.inactive_users; 
            console.log('Fetched inactive users:', this.inactiveUsers);
          }
        } catch (error) {
          console.error('Error fetching inactive users:', error);
          if (error.response) {
            this.showErrorAlert(error.response.data.message);
          } else {
            this.showErrorAlert('Error fetching inactive users. Please try again.');
          }
        }
      },

      showInactivUsersModal() {
        this.showInactiveUsersModal = true;
      },

      closeInactiveUsersModal() {
        this.showInactiveUsersModal = false;
      },

},
  mounted(){
    this.fetchUsers();
    this.fetchInactiveUsers();

    this.$watch('showTable', () => {
    this.fetchUsers();
  });
  }
}

</script>