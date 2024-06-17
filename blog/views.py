from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.forms import RecordAddForm
from blog.models import Blog
from e_mail.services import get_cache_mailing_active, get_mailing_count_from_cache, get_cache_unique_quantity


# Create your views here.

class BlogView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_quantity_active'] = get_cache_mailing_active()
        context['mailing_quantity'] = get_mailing_count_from_cache()
        context['clients_unique_quantity'] = get_cache_unique_quantity()
        context['records'] = Blog.objects.order_by('?')[:3]

        return context


class BlogCreateView(CreateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    form_class = RecordAddForm
    success_url = reverse_lazy('blog:home')


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'objects_list'

    def get_object(self, queryset=None):
        self.object = super().get_object()
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    template_name = 'blog/blog_update_form.html'
    form_class = RecordAddForm
    success_url = reverse_lazy('blog:view_record')


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:home')


def toggle_published(request, pk):
    record_item = get_object_or_404(Blog, pk=pk)
    if record_item.is_published:
        record_item.is_published = False
    else:
        record_item.is_published = True

    record_item.save()

    return redirect(reverse('blog:home'))
