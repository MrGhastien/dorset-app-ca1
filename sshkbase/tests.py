import random

from django.contrib import auth
from django.test import TestCase
from .models import *
from django.urls import reverse, reverse_lazy

rand = random.Random()

PERM_READ = 1
PERM_WRITE = 2


def getRandom(l):
    return l[rand.randint(0, len(l) - 1)]


def standardSetUp():
    user1 = User.objects.create_user('epic-gamer', 'EPIC GAMER', 'gamer', 'test@example.com')
    user2 = User.objects.create_user('normal-user2445', 'normal guy', 'secure-password', 'normal@example.com')
    user3 = User.objects.create_superuser('testadmin', 'ADMINISTRATORATOR', 'adminadmin', 'admin@django.gov')
    SSHKey.objects.create(user=user1, title='key1', key='KEY ABC', permissions=3)
    SSHKey.objects.create(user=user2, title='key2', key='KEY DEF', permissions=2)
    SSHKey.objects.create(user=user3, title='key3', key='KEY GHI', permissions=1)


# Create your tests here.

class UserTests(TestCase):

    def setUp(self):
        standardSetUp()

    def testGet(self):
        user = User.objects.get(nickname='epic-gamer')
        self.assertEqual(user.name, "EPIC GAMER")
        user = User.objects.get(nickname='normal-user2445')
        self.assertEqual(user.name, "normal guy")
        user = User.objects.get(nickname='testadmin')
        self.assertEqual(user.name, "ADMINISTRATORATOR")
        users = User.objects.all()
        self.assertEqual(len(users), 3)

    def testDelete(self):
        user = User.objects.get(nickname='epic-gamer')
        user.delete()
        self.assertRaises(User.DoesNotExist, lambda: User.objects.get(nickname='epic-gamer'))


class SSHKeyTests(TestCase):

    def setUp(self) -> None:
        standardSetUp()

    def testGet(self):
        keys = SSHKey.objects.filter(user__nickname='epic-gamer')
        self.assertEqual(keys[0].key, 'KEY ABC')
        self.assertEqual(len(keys), 1)

    def testDelete(self):
        key1 = SSHKey.objects.get(key='KEY ABC')
        key1.delete()
        self.assertRaises(SSHKey.DoesNotExist, lambda: SSHKey.objects.get(key='KEY ABC'))


class BasicViewTests(TestCase):

    def setUp(self):
        standardSetUp()

    def testIndex(self):
        response = self.client.get(reverse('sshkbase:index'))
        self.assertTemplateUsed(response, 'sshkbase/index-anonymous.html')

        self.client.login(nickname='epic-gamer', password='gamer')
        response = self.client.get(reverse('sshkbase:index'))
        self.assertTemplateUsed(response, 'sshkbase/index.html')

    def testList(self):
        response = self.client.get(reverse('sshkbase:list'))
        self.assertTemplateUsed(response, 'sshkbase/list.html')

    def testUserAdd(self):
        response = self.client.get(reverse('sshkbase:user-new'))
        self.assertTemplateUsed(response, 'sshkbase/userInfo/userAdd.html')

    def testUserDelete(self):
        self.client.login(nickname='epic-gamer', password='gamer')
        response = self.client.get(reverse('sshkbase:user-delete'))
        self.assertTemplateUsed(response, 'sshkbase/userInfo/userDelete.html')

        self.client.logout()
        response = self.client.get(reverse('sshkbase:user-delete'))
        self.assertRedirects(response, reverse('sshkbase:index'))

    def testLogin(self):
        response = self.client.get(reverse('sshkbase:user-login'))
        self.assertTemplateUsed(response, 'sshkbase/userInfo/userLogin.html')

    def testUserDetail(self):
        self.client.login(nickname='epic-gamer', password='gamer')
        response = self.client.get(reverse('sshkbase:user-detail', args=('normal-user2445',)))
        self.assertTemplateUsed(response, 'sshkbase/userInfo/userDetail.html')

    def testUpdateUser(self):
        self.client.login(nickname='normal-user2445', password='secure-password')
        response = self.client.get(reverse('sshkbase:user-update'))
        self.assertTemplateUsed(response, 'sshkbase/userInfo/userUpdate.html')

        self.client.logout()
        response = self.client.get(reverse('sshkbase:user-delete'))
        self.assertRedirects(response, reverse('sshkbase:index'))

    def testKeyList(self):
        self.client.login(nickname='normal-user2445', password='secure-password')
        response = self.client.get(reverse('sshkbase:user-keys'))
        self.assertTemplateUsed(response, 'sshkbase/userInfo/userKeys.html')

        self.client.logout()
        response = self.client.get(reverse('sshkbase:user-delete'))
        self.assertRedirects(response, reverse('sshkbase:index'))

    def testPasswordUpdate(self):
        self.client.login(nickname='normal-user2445', password='secure-password')
        response = self.client.get(reverse('sshkbase:user-update-password'))
        self.assertTemplateUsed(response, 'registration/password-change.html')

        self.client.logout()
        response = self.client.get(reverse('sshkbase:user-delete'))
        self.assertRedirects(response, reverse('sshkbase:index'))

    def testKeyAdd(self):
        self.client.login(nickname='normal-user2445', password='secure-password')
        response = self.client.get(reverse('sshkbase:add-key'))
        self.assertTemplateUsed(response, 'sshkbase/keyInfo/keyAdd.html')

        self.client.logout()
        response = self.client.get(reverse('sshkbase:user-delete'))
        self.assertRedirects(response, reverse('sshkbase:index'))

    def testKeyDetail(self):
        self.client.login(nickname='normal-user2445', password='secure-password')
        response = self.client.get(reverse('sshkbase:key-detail', args=(getRandom(SSHKey.objects.all()).id,)))
        self.assertTemplateUsed(response, 'sshkbase/keyInfo/keyDetail.html')

    def testKeyDelete(self):
        self.client.login(nickname='normal-user2445', password='secure-password')
        response = self.client.get(reverse('sshkbase:key-delete', args=(getRandom(SSHKey.objects.all()).id,)))
        self.assertTemplateUsed(response, 'sshkbase/keyInfo/keyDelete.html')

        self.client.logout()
        response = self.client.get(reverse('sshkbase:user-delete'))
        self.assertRedirects(response, reverse('sshkbase:index'))


class PostHandlerTests(TestCase):

    def setUp(self):
        standardSetUp()

    def testAddUser(self):
        response = self.client.post('/new-user/send', {
            'nickname': 'test-user',
            'full-name': 'TESTER',
            'email': 'email@example.xyz',
            'password': 'cool-password56'
        })
        self.assertRedirects(response, reverse('sshkbase:index'))
        User.objects.get(nickname='test-user')

        response = self.client.post('/new-user/send', {
            'nickname': 'test-user',
            'full-name': 'gg',
            'email': 'email@example.xyz',
            'password': 'co'
        })
        self.assertTemplateUsed(response, 'sshkbase/userInfo/userAdd.html')  # Failed to create user

    def testLogin(self):
        response = self.client.post('/login/send', {
            'nickname': 'normal-user2445',
            'password': 'secure-password'
        })
        self.assertRedirects(response, reverse('sshkbase:index'))
        user = auth.get_user(self.client)
        assert user.is_authenticated
        self.client.logout()

        response = self.client.post('/login/send', {
            'nickname': 'test-user',
            'password': 'co'
        })
        self.assertTemplateUsed(response, 'sshkbase/userInfo/userLogin.html')  # Failed to create user
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def testLogout(self):
        # test when logged in
        self.client.login(nickname='normal-user2445', password='secure-password')
        response = self.client.get('/logout')
        self.assertRedirects(response, reverse('sshkbase:index'))
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

        # test when not logged in
        response = self.client.get('/logout')
        self.assertRedirects(response, reverse('sshkbase:index'))
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def testUpdateUser(self):
        self.client.login(nickname='normal-user2445', password='secure-password')
        response = self.client.post('/update-user/send', {
            'name': 'NEW NAME'
        })
        self.assertRedirects(response, reverse('sshkbase:user-detail', args=('normal-user2445',)))
        self.assertEqual(User.objects.get(nickname='normal-user2445').name, "NEW NAME")
        self.client.logout()

        response = self.client.post('/update-user/send', {
            'name': 'NEW NAME 2'
        })
        self.assertRedirects(response, reverse('sshkbase:index'))

    def testDeleteUser(self):
        self.client.login(nickname='normal-user2445', password='secure-password')
        response = self.client.post('/delete-user/send', {})
        self.assertRedirects(response, reverse('sshkbase:index'))
        self.assertRaises(User.DoesNotExist, lambda: User.objects.get(nickname='normal-user2445'))

        response = self.client.post('/delete-user/send', {})
        User.objects.get(nickname='epic-gamer')
        User.objects.get(nickname='testadmin')
        self.assertRedirects(response, reverse('sshkbase:index'))

    def testUpdatePassword(self):
        self.client.login(nickname='normal-user2445', password='secure-password')
        # valid password
        response = self.client.post('/update-user/password/send', {
            'password': 'ashjkdbihjas',
            'password-confirm': 'ashjkdbihjas'
        })
        self.assertRedirects(response, reverse('sshkbase:index'))
        self.client.logout()
        self.assertFalse(self.client.login(nickname='normal-user2445', password='secure-password'))
        self.assertTrue(self.client.login(nickname='normal-user2445', password='ashjkdbihjas'))
        # Passwords are not matching
        response = self.client.post('/update-user/password/send', {
            'password': 'zziikfdnasdi',
            'password-confirm': 'not-matching'
        })
        self.assertTemplateUsed(response, 'registration/password-change.html')
        self.client.logout()
        self.assertFalse(self.client.login(nickname='normal-user2445', password='zziikfdnasdi'))
        self.assertFalse(self.client.login(nickname='normal-user2445', password='not-matching'))
        self.assertTrue(self.client.login(nickname='normal-user2445', password='ashjkdbihjas'))
        # Invalid password
        response = self.client.post('/update-user/password/send', {
            'password': 'test',
            'password-confirm': 'test'
        })
        self.assertTemplateUsed(response, 'registration/password-change.html')
        self.client.logout()
        self.assertFalse(self.client.login(nickname='normal-user2445', password='test'))
        self.assertTrue(self.client.login(nickname='normal-user2445', password='ashjkdbihjas'))

    def testAddKey(self):
        self.client.login(nickname='normal-user2445', password='secure-password')
        response = self.client.post('/new-key/send', {
            'title': 'test title',
            'key': 'key abcdefghijklmnopqrstuvwxyz',
            'perm-write': 'on'
        })
        self.assertRedirects(response, reverse('sshkbase:user-keys'))
        key = SSHKey.objects.get(title='test title')
        self.assertEqual(key.permissions, 2)
        self.assertEqual(key.key, 'key abcdefghijklmnopqrstuvwxyz')

        response = self.client.post('/new-key/send', {
            'title': '    ',
            'key': 'key abcdefghijklmnopqrstuvwxyz',
            'perm-read': 'on'
        })
        self.assertTemplateUsed(response, 'sshkbase/keyInfo/keyAdd.html')

    def testUpdateKey(self):
        self.client.login(nickname='normal-user2445', password='secure-password')
        key1 = SSHKey.objects.get(title='key1')
        id = key1.id
        response = self.client.post(reverse('sshkbase:key-update', args=(id,)), {
            'title': 'key8890',
            'key': 'key abcdefghijklmnopqrstuvwxyz',
            'perm-write': 'on'
        })
        key1 = SSHKey.objects.get(id=id)
        self.assertEqual(key1.title, 'key8890')
        self.assertEqual(key1.key, 'key abcdefghijklmnopqrstuvwxyz')
        self.assertEqual(key1.permissions, PERM_WRITE)
        self.assertRedirects(response, reverse('sshkbase:user-keys'))

        response = self.client.post(reverse('sshkbase:key-update', args=(id,)), {
            'title': '',
            'key': 'key other',
            'perm-read': 'on'
        })
        key1 = SSHKey.objects.get(id=id)
        self.assertEqual(key1.title, 'key8890')
        self.assertEqual(key1.key, 'key abcdefghijklmnopqrstuvwxyz')
        self.assertEqual(key1.permissions, PERM_WRITE)
        self.assertTemplateUsed(response, 'sshkbase/keyInfo/keyDetail.html')

        response = self.client.post(reverse('sshkbase:key-update', args=(id,)), {
            'title': 'key1',
            'key': '',
            'perm-read': 'on'
        })
        key1 = SSHKey.objects.get(id=id)
        self.assertEqual(key1.title, 'key8890')
        self.assertEqual(key1.key, 'key abcdefghijklmnopqrstuvwxyz')
        self.assertEqual(key1.permissions, PERM_WRITE)
        self.assertTemplateUsed(response, 'sshkbase/keyInfo/keyDetail.html')

    def testDeleteKey(self):
        self.client.login(nickname='normal-user2445', password='secure-password')
        key1 = SSHKey.objects.get(title='key1')
        response = self.client.post(reverse('sshkbase:key-delete-send', args=(key1.id,)), {})
        self.assertRedirects(response, reverse('sshkbase:user-keys'))
        self.assertRaises(SSHKey.DoesNotExist, lambda: SSHKey.objects.get(id=key1.id))

        response = self.client.post(reverse('sshkbase:key-delete-send', args=(123456789,)), {})
        self.assertEqual(response.status_code, 404)
