from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse
from time import timezone
import markdown
from django.utils.html import strip_tags


class BaseModel(models.Model):
    create_time = models.DateTimeField(default=datetime.now,
                                       verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name='更新时间')  # 最后更新时间

    class Meta:
        abstract = True


class Category(BaseModel):
    """
    django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    当然 django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
    django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100, verbose_name='分类名称')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(BaseModel):
    """
    标签 Tag 也比较简单，和 Category 一样。
    再次强调一定要继承 models.Model 类！
    """
    name = models.CharField(max_length=100, verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(BaseModel):
    """
    文章的数据库表稍微复杂一点，主要是涉及的字段更多。
    """

    # 文章标题
    title = models.CharField(max_length=70, verbose_name='文章标题')

    # 文章正文，我们使用了 TextField。
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    body = models.TextField(verbose_name='文章正文')
    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='正文内容')

    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一
    # 对多的关联关系。且自 django 2.0 以后，ForeignKey 必须传入一个 on_delete 参数用来指定当关联的
    # 数据被删除时，被关联的数据的行为，我们这里假定当某个分类被删除时，该分类下全部文章也同时被删除，因此     # 使用 models.CASCADE 参数，意为级联删除。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用
    # ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/2.2/topics/db/models/#relationships
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='文章所属分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='文章所属标签')

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是
    # django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和
    # Category 类似。
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='作者')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        print('*' * 10)
        print(self.pk)
        return reverse('blog_2:detail', kwargs={'pk': self.pk})

    # def save(self, *args, **kwargs):
    #     self.update_time = timezone.now()
    #
    #     # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
    #     # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
    #     md = markdown.Markdown(extensions=[
    #         'markdown.extensions.extra',
    #         'markdown.extensions.codehilite',
    #     ])
    #
    #     # 先将 Markdown 文本渲染成 HTML 文本
    #     # strip_tags 去掉 HTML 文本的全部 HTML 标签
    #     # 从文本摘取前 54 个字符赋给 excerpt
    #
    #     # 好像没有判断如果如果手动输入摘要时的情况啊
    #     # self.excerpt = strip_tags(md.convert(self.body))[:54]
    #     super().save(*args, **kwargs)
