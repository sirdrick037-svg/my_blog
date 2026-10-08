from types import SimpleNamespace

from django.template.loader import render_to_string
from django.urls import reverse
from django.test import SimpleTestCase, TestCase
from django.contrib.auth.models import User

from .forms import PostForm, SubscribeForm
from .models import Author, Post, Subscriber


class PostImageRenderingTests(SimpleTestCase):
    def test_image_is_rendered_on_blog_detail(self):
        post = SimpleNamespace(
            title='A test post',
            content='Post content',
            image=SimpleNamespace(url='https://example.com/post.jpg'),
        )

        html = render_to_string('blog_detail.html', {'post': post})

        self.assertContainsImage(html, 'https://example.com/post.jpg')

    def test_image_is_rendered_on_blog_list(self):
        post = SimpleNamespace(
            title='A test post',
            content='Post content',
            slug='a-test-post',
            image=SimpleNamespace(url='https://example.com/post.jpg'),
        )

        html = render_to_string('blogs.html', {'posts': [post]})

        self.assertContainsImage(html, 'https://example.com/post.jpg')

    def assertContainsImage(self, html, image_url):
        self.assertIn('<img', html)
        self.assertIn(image_url, html)


class BlogHomePageTests(TestCase):
    def test_root_url_shows_home_page_content(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'She went to the bank')

    def test_read_article_link_opens_post_detail(self):
        author = Author.objects.create(
            first_name='Blog',
            last_name='Writer',
            email='writer@example.com',
        )
        post = Post.objects.create(
            author=author,
            title='A test post',
            content='Post content',
            status=Post.Status.PUBLISHED,
        )

        listing_response = self.client.get(reverse('blogs'))
        detail_url = reverse('blog_detail', kwargs={'slug': post.slug})

        self.assertContains(listing_response, f'href="{detail_url}"')

        detail_response = self.client.get(detail_url)

        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, 'Post content')

    def test_blog_listing_shows_published_posts_and_drafts(self):
        author = Author.objects.create(
            first_name='Blog',
            last_name='Writer',
            email='writer@example.com',
        )
        Post.objects.create(
            author=author,
            title='Published admin post',
            content='Published content',
            status=Post.Status.PUBLISHED,
        )
        Post.objects.create(
            author=author,
            title='Draft admin post',
            content='Draft content',
            status=Post.Status.DRAFT,
        )

        response = self.client.get(reverse('blogs'))

        self.assertContains(response, 'PUBLISHED ADMIN POST')
        self.assertContains(response, 'DRAFT ADMIN POST')


class PostCreationTests(TestCase):
    def test_post_form_includes_image_field(self):
        self.assertIn('image', PostForm().fields)

    def test_create_post_assigns_author_from_logged_in_user(self):
        user = User.objects.create_user(
            username='writer',
            email='writer@example.com',
            first_name='Blog',
            last_name='Writer',
            password='test-password',
        )
        self.client.force_login(user)

        response = self.client.post(
            '/blogs/create/',
            {
                'title': 'A test post',
                'excerpt': '',
                'content': 'Post content',
                'category': '',
                'status': Post.Status.DRAFT,
                'published_at': '',
                'featured': '',
            },
        )

        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(slug='a-test-post')
        self.assertEqual(post.author, Author.objects.get(email='writer@example.com'))


class SubscriptionTests(TestCase):
    def test_subscribe_page_loads(self):
        response = self.client.get(reverse('subscribe'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Join the list')
        self.assertIsInstance(response.context['form'], SubscribeForm)

    def test_valid_email_creates_subscriber(self):
        response = self.client.post(
            reverse('subscribe'),
            {'email': 'reader@example.com'},
        )

        self.assertRedirects(response, reverse('subscribe'))
        self.assertTrue(
            Subscriber.objects.filter(email='reader@example.com').exists()
        )
