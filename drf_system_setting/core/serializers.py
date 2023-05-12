from rest_framework import fields, serializers


class CustomDisplayChoiceField(fields.ChoiceField):
    def to_representation(self, value):
        if value in ("", None):
            return {}
        return {"id": value, "label": dict(self.choices).get(value)}


class CustomDisplayMultipleChoiceField(fields.MultipleChoiceField):
    def to_representation(self, value):
        if value in ("", None):
            return []
        value = value.split(",")
        return [{"id": v, "label": dict(self.choices).get(v)} for v in value]


class ListTreePathSerializer(serializers.ListSerializer):
    def recursive_path(self, instance):
        tree_path = []
        tree_path.append(instance.name)
        if not instance.parent_id:
            return tree_path
        parent_path = self.recursive_path(self.results_map[instance.parent_id])

        return parent_path + tree_path

    def to_representation(self, instance):
        self.results_map = {i.pk: i for i in self.child.Meta.model.objects.all()}

        results = []
        for i in instance:
            res = self.child.to_representation(i)
            res["tree_path"] = self.recursive_path(i)
            results.append(res)
        return results
