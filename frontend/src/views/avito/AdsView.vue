<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Объявления Avito</h2>
      <button @click="showForm = !showForm" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        {{ showForm ? 'Отмена' : '+ Создать' }}
      </button>
    </div>

    <form v-if="showForm" @submit.prevent="addAd" class="bg-white p-4 rounded shadow mb-6 space-y-3">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <select v-model="form.account_id" class="border rounded p-2" required>
          <option value="">Выберите аккаунт</option>
          <option v-for="acc in avitoStore.accounts" :key="acc.id" :value="acc.id">{{ acc.name }}</option>
        </select>
        <input v-model="form.title" placeholder="Заголовок" class="border rounded p-2" required />
        <input v-model.number="form.price" placeholder="Цена" type="number" class="border rounded p-2" />
        <input v-model="form.category" placeholder="Категория" class="border rounded p-2" />
        <input v-model="form.campaign" placeholder="Кампания" class="border rounded p-2" />
      </div>
      <textarea v-model="form.description" placeholder="Описание" class="w-full border rounded p-2" rows="3" required></textarea>
      <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded">Создать</button>
    </form>

    <div class="bg-white rounded shadow overflow-hidden">
      <table class="w-full text-left">
        <thead class="bg-gray-50">
          <tr>
            <th class="p-3">ID</th>
            <th class="p-3">Заголовок</th>
            <th class="p-3">Цена</th>
            <th class="p-3">Статус</th>
            <th class="p-3">Кампания</th>
            <th class="p-3">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ad in avitoStore.ads" :key="ad.id" class="border-t">
            <td class="p-3">{{ ad.id }}</td>
            <td class="p-3">{{ ad.title }}</td>
            <td class="p-3">{{ ad.price ? ad.price + ' ₽' : '—' }}</td>
            <td class="p-3">
              <span class="px-2 py-1 rounded text-xs" :class="{
                'bg-green-100 text-green-700': ad.status === 'active',
                'bg-gray-100 text-gray-700': ad.status === 'draft',
                'bg-red-100 text-red-700': ad.status === 'blocked',
                'bg-yellow-100 text-yellow-700': ad.status === 'archived',
              }">{{ ad.status }}</span>
            </td>
            <td class="p-3">{{ ad.campaign || '—' }}</td>
            <td class="p-3 space-x-2">
              <button v-if="ad.status === 'draft'" @click="avitoStore.publishAd(ad.id)" class="text-blue-600 hover:underline">Опубликовать</button>
              <button @click="avitoStore.deleteAd(ad.id)" class="text-red-600 hover:underline">Удалить</button>
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

const avitoStore = useAvitoStore()
const showForm = ref(false)
const form = ref({ account_id: '', title: '', description: '', price: null, category: '', campaign: '' })

const addAd = async () => {
  await avitoStore.createAd(form.value)
  form.value = { account_id: '', title: '', description: '', price: null, category: '', campaign: '' }
  showForm.value = false
}

onMounted(() => { avitoStore.fetchAds(); avitoStore.fetchAccounts() })
</script>
