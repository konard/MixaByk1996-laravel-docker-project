<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Аккаунты Avito</h2>
      <button @click="showForm = !showForm" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        {{ showForm ? 'Отмена' : '+ Добавить' }}
      </button>
    </div>

    <form v-if="showForm" @submit.prevent="addAccount" class="bg-white p-4 rounded shadow mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
      <input v-model="form.name" placeholder="Название" class="border rounded p-2" required />
      <input v-model="form.client_id" placeholder="Client ID" class="border rounded p-2" required />
      <input v-model="form.client_secret" placeholder="Client Secret" type="password" class="border rounded p-2" required />
      <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">Сохранить</button>
    </form>

    <div class="bg-white rounded shadow overflow-hidden">
      <table class="w-full text-left">
        <thead class="bg-gray-50">
          <tr>
            <th class="p-3">ID</th>
            <th class="p-3">Название</th>
            <th class="p-3">Client ID</th>
            <th class="p-3">Статус</th>
            <th class="p-3">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="acc in store.accounts" :key="acc.id" class="border-t">
            <td class="p-3">{{ acc.id }}</td>
            <td class="p-3">{{ acc.name }}</td>
            <td class="p-3">{{ acc.client_id }}</td>
            <td class="p-3">
              <span :class="acc.is_active ? 'text-green-600' : 'text-red-600'">
                {{ acc.is_active ? 'Активен' : 'Неактивен' }}
              </span>
            </td>
            <td class="p-3">
              <button @click="store.deleteAccount(acc.id)" class="text-red-600 hover:underline">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAvitoStore } from '../../store'

const store = useAvitoStore()
const showForm = ref(false)
const form = ref({ name: '', client_id: '', client_secret: '' })

const addAccount = async () => {
  await store.createAccount(form.value)
  form.value = { name: '', client_id: '', client_secret: '' }
  showForm.value = false
}

onMounted(() => store.fetchAccounts())
</script>
