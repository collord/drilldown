from trame.widgets import vuetify
import uuid
import time
import numpy as np

from ..layer.layer import IntervalDataLayer, PointDataLayer


class LayerUI(vuetify.VCard):
    def __init__(self, layer):
        super().__init__(
            classes="mb-2",
            elevation=0,
            style="background-color: #f5f5f5;",
            click=self.on_layer_click,
        )
        self.layer = layer
        self.name = layer.name
        self.state = layer.state
        self.id = uuid.uuid4().hex

        self.state[f"visibility_{self.id}"] = self.layer.visibility

        # for tracking ~simultaneous visibility button and layer click events
        self.visibility_button_click_timestamp = np.inf
        self.layer_click_timestamp = np.inf

        with self:
            with vuetify.VRow(
                classes="ma-0 pa-0 d-flex align-center",
            ):
                with vuetify.VCol(
                    cols="2",
                    classes="ma-0 pa-0",
                ):
                    with vuetify.VBtn(
                        icon=True,
                        classes="ma-0 pa-0",
                    ) as self.visibility_button:
                        vuetify.VIcon(
                            "mdi-eye",
                            classes="ma-0 pa-0",
                            v_if=f"visibility_{self.id}",
                            click=(self.on_visibility_button_click),
                        )
                        vuetify.VIcon(
                            "mdi-eye-off",
                            classes="ma-0 pa-0",
                            v_if=f"!visibility_{self.id}",
                            click=(self.on_visibility_button_click),
                        )

                with vuetify.VCol(
                    cols="8",
                    classes="ma-0 pa-0",
                ):
                    vuetify.VCardText(
                        self.name,
                        classes="py-2 ma-0 pa-0 text-center",
                        style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;",
                    )

                with vuetify.VCol(
                    cols="2",
                    classes="ma-0 pa-0",
                ):
                    icon_style = ""
                    if isinstance(self.layer, IntervalDataLayer):
                        icon_name = "mdi-ladder"
                    elif isinstance(self.layer, PointDataLayer):
                        icon_name = "mdi-ray-start-vertex-end"
                        icon_style += "transform: rotate(90deg);"

                    vuetify.VIcon(
                        icon_name,
                        style=icon_style,
                        classes="ma-0 pa-0",
                    )

    def on_layer_click(self):
        self.layer_click_timestamp = time.time()

        if (
            abs(self.layer_click_timestamp - self.visibility_button_click_timestamp)
            > 0.1
        ):
            self.state.ctrl_mesh_name = self.name

    def on_visibility_button_click(self):
        self.visibility_button_click_timestamp = time.time()

        self.layer.visibility = not self.layer.visibility
        self.state[f"visibility_{self.id}"] = self.layer.visibility


class LayerListUI(vuetify.VContainer):
    def __init__(self):
        super().__init__(
            fluid=True,
            style="display: flex; flex-direction: column; overflow: auto; height: 50%; width: 90%;",
        )
        with self:
            with vuetify.VRow(style="overflow: auto;"):
                self.layer_list = vuetify.VCol(classes="ma-0 pa-0")

    def add_layer(self, layer):
        layer_ui = LayerUI(layer)
        self.layer_list.add_child(layer_ui)

    @property
    def layers(self):
        return self.layer_list.children
