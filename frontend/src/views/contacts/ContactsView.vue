<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Контакты</h2>
      <div class="space-x-2">
        <button @click="showImport = !showImport" class="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700">Импорт CSV/Excel</button>
        <button @click="showForm = !showForm" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          {{ showForm ? 'Отмена' : '+ Добавить' }}
        </button>
      </div>
    </div>

    <div v-if="showImport" class="bg-white p-4 rounded shadow mb-6">
      <p class="mb-2 text-sm text-gray-600">Загрузите CSV или Excel файл с колонками: email, name, phone, city, interests</p>
      <input type="file" @change="handleFile" accept=".csv,.xlsx,.xls" class="border rounded p-2" />
      <div v-if="importResult" class="mt-2 text-sm">
        <p class="text-green-600">Импортировано: {{ importResult.imported }}</p>
        <p class="text-yellow-600">Пропущено: {{ importResult.skipped }}</p>
        <p v-if="importResult.errors.length" class="text-red-600">Ошибки: {{ importResult.errors.join(', ') }}</p>
      </div>
    </div>

    <form v-if="showForm" @submit.prevent="addContact" class="bg-white p-4 rounded shadow mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
      <input v-model="form.email" placeholder="Email" type="email" class="border rounded p-2" required />
      <input v-model="form.name" placeholder="Имя" class="border rounded p-2" />
      <input v-model="form.phone" placeholder="Телефон" class="border rounded p-2" />
      <input v-model="form.city" placeholder="Город" class="border rounded p-2" />
      <label class="flex items-center gap-2"><input type="checkbox" v-model="form.consent_given" /> Согласие на обработку данных</label>
      <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded">Добавить</button>
    </form>

    <div class="bg-white rounded shadow overflow-hidden">
      <table class="w-full text-left">
        <thead class="bg-gray-50"><tr><th class="p-3">ID</th><th class="p-3">Email</th><th class="p-3">Имя</th><th class="p-3">Город</th><th class="p-3">Подписка</th><th class="p-3">Действия</th></tr></thead>
        <tbody>
          <tr v-for="c in store.contacts" :key="c.id" class="border-t">
            <td class="p-3">{{ c.id }}</td><td class="p-3">{{ c.email }}</td><td class="p-3">{{ c.name || '—' }}</td>
            <td class="p-3">{{ c.city || '—' }}</td>
            <td class="p-3"><span :class="c.is_subscribed ? 'text-green-600' : 'text-red-600'">{{ c.is_subscribed ? 'Да' : 'Нет' }}</span></td>
            <td class="p-3"><button @click="store.deleteContact(c.id)" class="text-red-600 hover:underline">Удалить</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useContactStore } from '../../store'
const store = useContactStore()
const showForm = ref(false)
const showImport = ref(false)
const importResult = ref(null)
const form = ref({ email: '', name: '', phone: '', city: '', consent_given: false })

const addContact = async () => {
  await store.createContact(form.value)
  form.value = { email: '', name: '', phone: '', city: '', consent_given: false }
  showForm.value = false
}

const handleFile = async (e) => {
  const file = e.target.files[0]
  if (file) {
    importResult.value = await store.importContacts(file)
    await store.fetchContacts()
  }
}

onMounted(() => store.fetchContacts())
</script>
